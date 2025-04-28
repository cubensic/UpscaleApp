from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import imghdr
from backend.config.settings import settings
from PIL import Image
import io
from typing import List
import logging
import os

app = FastAPI(title="Simple Image Upscaler")

# Mount the public directory as static files at the root
app.mount("/", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "../public"), html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # Set this in your .env for production, e.g. ["https://yourfrontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPPORTED_FORMATS = {"jpeg", "png", "webp", "bmp", "tiff"}

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.env == "development" else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/upscale")
async def upscale_image(file: List[UploadFile] = File(...)):
    logging.info(f"Received request to /api/upscale with {len(file)} file(s)")
    if len(file) != 1:
        logging.warning("Validation failed: Multiple or no files uploaded.")
        raise HTTPException(status_code=400, detail="Please upload a single image file.")
    file = file[0]
    # --- Robust file size check ---
    # Check the raw upload size (if available)
    if hasattr(file, 'spool_max_size') and hasattr(file.file, 'tell'):
        pos = file.file.tell()
        file.file.seek(0, 2)  # Seek to end
        raw_size = file.file.tell()
        file.file.seek(pos)   # Restore position
        if raw_size > 10 * 1024 * 1024:
            logging.warning(f"Validation failed: File too large (raw upload {raw_size} bytes).")
            raise HTTPException(status_code=400, detail="File too large (max 10MB).")
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        logging.warning(f"Validation failed: File too large (buffer {len(contents)} bytes).")
        raise HTTPException(status_code=400, detail="File too large (max 10MB).")
    # Validate file type
    if not file.content_type.startswith("image/"):
        logging.warning(f"Validation failed: Unsupported file type {file.content_type}.")
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    # Check format
    fmt = imghdr.what(None, h=contents)
    if fmt not in SUPPORTED_FORMATS:
        logging.warning(f"Validation failed: Unsupported image format {fmt}.")
        raise HTTPException(status_code=400, detail="Unsupported image format.")
    # Upscale using Pillow
    try:
        img = Image.open(io.BytesIO(contents))
        new_size = (img.width * 2, img.height * 2)
        upscaled = img.resize(new_size, resample=Image.LANCZOS)
        out_buf = io.BytesIO()
        # Map imghdr format to Pillow format
        format_map = {"jpeg": "JPEG", "png": "PNG", "webp": "WEBP", "bmp": "BMP", "tiff": "TIFF"}
        pillow_fmt = format_map.get(fmt, "PNG")
        upscaled.save(out_buf, format=pillow_fmt)
        out_buf.seek(0)
        logging.info(f"Successfully upscaled image {file.filename} to {new_size[0]}x{new_size[1]}")
    except Exception as e:
        logging.error(f"Error upscaling image {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Error upscaling image.")
    return StreamingResponse(out_buf, media_type=file.content_type, headers={"Content-Disposition": f"attachment; filename=upscaled_{file.filename}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=(settings.env == "development"),
    ) 