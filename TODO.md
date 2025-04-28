# To-Do List

---
**Current Status:**
- All core backend and frontend features are complete and tested.
- Dockerfile, CI/CD (GitHub Actions), and documentation are in place.
- Hosting will be on DigitalOcean (Droplet IP: 64.226.120.221).

**Where we stopped:**
- SSH access to the DigitalOcean server is not yet working (connection timed out).
- Deployment to production is pending until SSH access is resolved.

**Next steps:**
1. Resolve SSH access to the DigitalOcean droplet (check firewall, droplet status, and SSH service).
2. Deploy the app using Docker and your `.env` file.
3. (Recommended) Set up Nginx and HTTPS for secure access.
4. Point frontend to production backend URL and test live deployment.

---

# Deployment Issue (Vercel Python Serverless Function)

**Current Problem:**
- The deployed Python serverless function at `/api/upscale.py` fails with:
  `ModuleNotFoundError: No module named 'vercel_python'`
- This means Vercel is not recognizing the function as a serverless function and is not injecting the `vercel_python` module.

**What We Tried:**
- Verified `/api/upscale.py` exists and contains the correct handler.
- Ensured `/public/` contains all frontend files.
- Confirmed there is no `main.py`, `vercel.json`, or other custom server files in the root.
- Checked that `requirements.txt` contains only `pillow`.
- Removed unnecessary files and redeployed.
- Recommended a clean redeploy (delete Vercel project, re-import, redeploy).

**Next Steps:**
1. Delete the Vercel project from the dashboard to clear any cached configuration.
2. Double-check local project structure:
    - `/api/upscale.py` (with the correct handler)
    - `/public/` (with all frontend files)
    - `requirements.txt` (only `pillow`)
    - No `main.py`, `vercel.json`, or other Python files in the root.
3. Push the latest code to the Git repository.
4. Re-import the project into Vercel and deploy.
5. Test the deployed app at the Vercel URL.
6. If the error persists, check the Vercel build and runtime logs for any new clues.
7. If still unresolved, share the full file tree and any new error messages for further diagnosis.

---

## 1. Project Setup  
- [x] Initialize Git repository  
- [x] Create project directory structure  
- [x] Set up Python virtual environment  
- [x] Add `.env.template` for environment variables (dev/test/prod)  
- [x] Install core dependencies  
  - [x] Flask or FastAPI  
  - [x] Pillow (or AI upscaling library)  
  - [x] pytest  

## 2. Frontend  
### 2.1 HTML & CSS  
- [x] Create `index.html` with basic layout  
- [x] Style drag-and-drop area, preview container, result container  
- [x] Ensure responsive design for mobile and desktop  

### 2.2 JavaScript  
- [x] Implement drag-and-drop file upload  
- [x] Implement file picker fallback  
- [x] Enforce single-file upload, file type (JPG/PNG/WEBP/TIFF/BMP), max size 10 MB  
- [x] Display thumbnail preview of uploaded image  
- [x] "Upscale" button click handler: send image to `/api/upscale`  
- [x] Show processing status ("Processing…")  
- [x] Display upscaled image preview and enable "Download" button  
- [x] Display error messages for invalid file, size limit, processing errors  

### 2.3 Accessibility  
- [x] Add ARIA labels to drop area and buttons  
- [x] Ensure keyboard navigation for all controls  

## 3. Backend  
### 3.1 Framework & Routing  
- [x] Initialize Flask/FastAPI application  
- [x] Define `POST /api/upscale` endpoint  

### 3.2 Validation & Processing  
- [x] Validate multipart request:  
  - [x] Single file only  
  - [x] Supported formats  
  - [x] File size ≤ 10 MB  
- [x] Load image in-memory (no persistent storage)  
- [x] Perform 2× upscaling (Pillow interpolation or AI model)  
- [x] Return upscaled image in original format as binary response  

### 3.3 Error Handling & Logging  
- [x] Return meaningful HTTP status codes and JSON error messages  
- [x] Log requests, validation failures, and processing errors  

## 4. Testing  
- [x] Configure pytest and test runner  
- [x] Write unit tests for `/api/upscale`:  
  - [x] Valid image processing  
  - [x] Invalid file type, oversize file, multiple files  
- [x] Write integration test for end-to-end upload → upscale → download  
- [ ] (Optional) Add frontend unit tests for validation logic  

## 5. Deployment & Environments  
- [x] Configure dev, test, and prod environment variables  
- [x] Create Dockerfile or serverless configuration  
- [x] Set up CI/CD pipeline for automated tests and deployment  
- [x] Provision hosting (DigitalOcean droplet)  

## 6. Documentation  
- [x] Write `README.md` with:  
  - [x] Project overview  
  - [x] Setup instructions  
  - [x] Environment configuration  
  - [x] Usage guide  
- [x] Document API endpoint in `docs/API.md`  
- [ ] Include screenshots or GIFs of the UI  

--- 