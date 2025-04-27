# API Documentation

## Endpoints

### 1. Health Check

**GET** `/health`

- **Description:** Returns a simple status message to verify the backend is running.
- **Response:**
  ```json
  { "status": "ok" }
  ```

---

### 2. Upscale Image

**POST** `/api/upscale`

- **Description:** Upload a single image file to upscale it by 2x. Returns the upscaled image in the same format.
- **Request:**
  - Content-Type: `multipart/form-data`
  - Body:
    - `file`: The image file to upscale (JPEG, PNG, WEBP, TIFF, BMP; max 10MB)

- **Response:**
  - Content-Type: `image/<format>`
  - Body: Binary image data (upscaled image)
  - Header: `Content-Disposition: attachment; filename=upscaled_<original_filename>`

- **Example (curl):**
  ```sh
  curl -F "file=@yourimage.jpg" http://localhost:8000/api/upscale --output upscaled_yourimage.jpg
  ```

#### Error Responses
| Status | Message                        | Description                        |
|--------|--------------------------------|------------------------------------|
| 400    | Please upload a single image…  | More than one or no file uploaded  |
| 400    | File too large (max 10MB).    | File exceeds 10MB                  |
| 400    | Unsupported file type.        | Not an image MIME type             |
| 400    | Unsupported image format.     | Not in supported formats           |
| 500    | Error upscaling image.        | Processing failed                  |

---

## Notes
- Only one file per request is supported.
- Supported formats: JPEG, PNG, WEBP, TIFF, BMP.
- Max file size: 10MB.
- All processing is in-memory; no files are stored on the server. 