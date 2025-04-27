# Simple Image Upscaler

A web application that allows users to upload a single image, upscale it by 2x, and download the result. Built with FastAPI (Python backend), HTML/JS frontend, and Pillow for image processing.

## Features
- Drag-and-drop or file picker upload
- Supports JPEG, PNG, WEBP, TIFF, BMP
- 2x upscaling (high-quality interpolation)
- Download upscaled image in original format
- No persistent storage; all processing is in-memory
- Docker-ready

## Quick Start (Local)

1. **Clone the repo:**
   ```sh
   git clone <your-repo-url>
   cd upscale-app
   ```
2. **Set up virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configure environment:**
   - Copy `.env.template` to `.env` and edit as needed.
4. **Run backend:**
   ```sh
   uvicorn backend.main:app --reload
   ```
5. **Open frontend:**
   - Open `frontend/index.html` in your browser (or serve with a static file server).

## Quick Start (Docker)

1. **Build and run:**
   ```sh
   docker build -t upscale-app .
   docker run -p 8000:8000 upscale-app
   ```
2. **Configure environment:**
   - Edit `.env` or set environment variables as needed.

## Environment Variables
- `ENV` - `development` or `production`
- `HOST` - Host for backend (default: `0.0.0.0`)
- `PORT` - Port for backend (default: `8000`)
- `CORS_ORIGINS` - JSON list of allowed origins (e.g. `["https://yourfrontend.com"]`)
- `MAX_FILE_SIZE` - Max upload size in bytes (default: `10485760`)

## API Usage
See [docs/API.md](docs/API.md) for full API documentation.

## Testing
```sh
pytest
```

## Deployment
- Use Docker for production deployment.
- Set environment variables appropriately for production.
- Restrict CORS in production.
- Set up HTTPS (reverse proxy or managed solution).

## License
MIT 