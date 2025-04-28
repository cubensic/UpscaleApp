import io
import imghdr
from PIL import Image
from vercel_python import Response

SUPPORTED_FORMATS = {"jpeg", "png", "webp", "bmp", "tiff"}

def handler(request):
    if request.method == "GET":
        return Response("OK", status=200)
    if request.method != "POST":
        return Response("Method Not Allowed", status=405)
    if not hasattr(request, "files") or "file" not in request.files:
        return Response("Please upload a single image file.", status=400)
    files = request.files.getlist("file")
    if len(files) != 1:
        return Response("Please upload a single image file.", status=400)
    file = files[0]
    contents = file.read()
    if len(contents) > 10 * 1024 * 1024:
        return Response("File too large (max 10MB).", status=400)
    fmt = imghdr.what(None, h=contents)
    if fmt not in SUPPORTED_FORMATS:
        return Response("Unsupported image format.", status=400)
    try:
        img = Image.open(io.BytesIO(contents))
        new_size = (img.width * 2, img.height * 2)
        upscaled = img.resize(new_size, resample=Image.LANCZOS)
        out_buf = io.BytesIO()
        format_map = {"jpeg": "JPEG", "png": "PNG", "webp": "WEBP", "bmp": "BMP", "tiff": "TIFF"}
        pillow_fmt = format_map.get(fmt, "PNG")
        upscaled.save(out_buf, format=pillow_fmt)
        out_buf.seek(0)
        return Response(
            out_buf.read(),
            status=200,
            headers={
                "Content-Type": file.content_type,
                "Content-Disposition": f"attachment; filename=upscaled_{file.filename}"
            }
        )
    except Exception as e:
        return Response(f"Error upscaling image: {str(e)}", status=500)
