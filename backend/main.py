from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import imghdr
from backend.config.settings import settings
from PIL import Image
import io

app = FastAPI(title="Simple Image Upscaler")

SUPPORTED_FORMATS = {"jpeg", "png", "webp", "bmp", "tiff"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/upscale")
async def upscale_image(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    # Read file in memory
    contents = await file.read()
    if len(contents) > settings.max_file_size:
        raise HTTPException(status_code=400, detail="File too large (max 10MB).")
    # Check format
    fmt = imghdr.what(None, h=contents)
    if fmt not in SUPPORTED_FORMATS:
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
    except Exception as e:
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