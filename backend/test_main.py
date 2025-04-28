import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from backend.main import app
from fastapi import HTTPException, UploadFile, File
import numpy as np

client = TestClient(app)


def create_test_image(format='PNG', size=(32, 32), color=(255, 0, 0)):
    img = Image.new('RGB', size, color)
    buf = io.BytesIO()
    img.save(buf, format=format)
    buf.seek(0)
    return buf


def test_upscale_valid_image():
    img_buf = create_test_image('PNG')
    response = client.post('/api/upscale', files={'file': ('test.png', img_buf, 'image/png')})
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('image/')
    assert response.content  # Should return image bytes


def test_upscale_invalid_file_type():
    fake_file = io.BytesIO(b'not an image')
    response = client.post('/api/upscale', files={'file': ('test.txt', fake_file, 'text/plain')})
    assert response.status_code == 400
    assert 'Unsupported file type' in response.text or 'unsupported' in response.text.lower()


def test_upscale_oversized_file():
    # Create a random image that will not compress well (BMP, >10MB)
    arr = np.random.randint(0, 256, (4000, 4000, 3), dtype=np.uint8)
    img = Image.fromarray(arr, 'RGB')
    buf = io.BytesIO()
    img.save(buf, format='BMP')  # BMP is uncompressed
    buf.seek(0)
    print("Test image size (bytes):", buf.getbuffer().nbytes)  # Optional: for debugging
    response = client.post('/api/upscale', files={'file': ('big.bmp', buf, 'image/bmp')})
    assert response.status_code == 400 or response.status_code == 413
    assert 'File too large' in response.text or 'too large' in response.text.lower()


def test_upscale_multiple_files():
    img1 = create_test_image('PNG')
    img2 = create_test_image('PNG')
    files = [
        ('file', ('img1.png', img1, 'image/png')),
        ('file', ('img2.png', img2, 'image/png')),
    ]
    response = client.post('/api/upscale', files=files)
    assert response.status_code == 400
    assert 'single image' in response.text.lower() or 'multiple' in response.text.lower()


def test_upscale_processing_failure(monkeypatch):
    from PIL import Image
    def fail_open(*args, **kwargs):
        raise Exception('Processing failed')
    monkeypatch.setattr(Image, 'open', fail_open)
    img_buf = create_test_image('PNG')
    response = client.post('/api/upscale', files={'file': ('test.png', img_buf, 'image/png')})
    assert response.status_code == 500
    assert 'error' in response.text.lower()


def test_upscale_oversized_file_with_check():
    # Create a fake image >10MB
    big_img = Image.new('RGB', (4000, 4000), (255, 0, 0))
    buf = io.BytesIO()
    big_img.save(buf, format='BMP')  # Use BMP for no compression
    buf.seek(0)
    if buf.getbuffer().nbytes > 10 * 1024 * 1024:
        response = client.post('/api/upscale', files={'file': ('big.bmp', buf, 'image/bmp')})
        assert response.status_code == 400 or response.status_code == 413
    else:
        assert False, "Test image is not large enough!"


@app.post("/api/upscale")
async def upscale_image(file: UploadFile = File(...)):
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB).")
    # ...rest of your processing logic... 