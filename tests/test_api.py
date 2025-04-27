import io
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def make_image_bytes(fmt="jpeg"):
    from PIL import Image
    buf = io.BytesIO()
    img = Image.new("RGB", (10, 10), color="red")
    img.save(buf, format=fmt.upper())
    buf.seek(0)
    return buf

def test_upscale_valid_jpeg():
    img = make_image_bytes("jpeg")
    response = client.post("/api/upscale", files={"file": ("test.jpg", img, "image/jpeg")})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/")

def test_upscale_invalid_type():
    response = client.post("/api/upscale", files={"file": ("test.txt", io.BytesIO(b"notanimage"), "text/plain")})
    assert response.status_code == 400
    assert "Unsupported file type" in response.text

def test_upscale_oversize():
    big = io.BytesIO(b"0" * (10485760 + 1))
    response = client.post("/api/upscale", files={"file": ("big.jpg", big, "image/jpeg")})
    assert response.status_code == 400
    assert "File too large" in response.text

def test_integration_upscale_flow():
    img = make_image_bytes("png")
    response = client.post("/api/upscale", files={"file": ("test.png", img, "image/png")})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/")
    # Check returned image is 2x size
    from PIL import Image
    out_img = Image.open(io.BytesIO(response.content))
    assert out_img.size == (20, 20)
    assert out_img.format == "PNG" 