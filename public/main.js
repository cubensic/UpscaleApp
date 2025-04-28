const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const previewImg = document.getElementById('preview');
const upscaleBtn = document.getElementById('upscale-btn');
const statusDiv = document.getElementById('status');
const resultImg = document.getElementById('result');
const downloadBtn = document.getElementById('download-btn');

let selectedFile = null;

function showStatus(msg, isError = false) {
  statusDiv.textContent = msg;
  statusDiv.style.color = isError ? '#c00' : '#222';
}

function resetPreview() {
  previewImg.style.display = 'none';
  previewImg.src = '';
  upscaleBtn.disabled = true;
  selectedFile = null;
}

dropArea.addEventListener('click', () => fileInput.click());
dropArea.addEventListener('keydown', e => {
  if (e.key === 'Enter' || e.key === ' ') fileInput.click();
});

dropArea.addEventListener('dragover', e => {
  e.preventDefault();
  dropArea.classList.add('dragover');
});
dropArea.addEventListener('dragleave', e => {
  e.preventDefault();
  dropArea.classList.remove('dragover');
});
dropArea.addEventListener('drop', e => {
  e.preventDefault();
  dropArea.classList.remove('dragover');
  handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', e => {
  handleFiles(e.target.files);
});

function handleFiles(files) {
  resetPreview();
  if (!files || files.length !== 1) {
    showStatus('Please select a single image file.', true);
    return;
  }
  const file = files[0];
  if (!/^image\/(jpeg|png|webp|bmp|tiff?)$/i.test(file.type)) {
    showStatus('Unsupported file type.', true);
    return;
  }
  if (file.size > 10485760) {
    showStatus('File too large (max 10MB).', true);
    return;
  }
  const reader = new FileReader();
  reader.onload = e => {
    previewImg.src = e.target.result;
    previewImg.style.display = 'block';
    upscaleBtn.disabled = false;
    selectedFile = file;
    showStatus('');
  };
  reader.readAsDataURL(file);
}

upscaleBtn.addEventListener('click', async () => {
  if (!selectedFile) return;
  showStatus('Processing...');
  upscaleBtn.disabled = true;
  resultImg.style.display = 'none';
  downloadBtn.style.display = 'none';
  downloadBtn.href = '';

  const formData = new FormData();
  formData.append('file', selectedFile);
  

  try {
    const response = await fetch('https://upscale-app-mocha.vercel.app/api/upscale', {
      method: 'POST',
      body: formData
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      showStatus(err.detail || 'Error upscaling image.', true);
      upscaleBtn.disabled = false;
      return;
    }
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    resultImg.src = url;
    resultImg.style.display = 'block';
    downloadBtn.href = url;
    downloadBtn.style.display = 'inline-block';
    showStatus('');
  } catch (e) {
    showStatus('Network or server error.', true);
    upscaleBtn.disabled = false;
  }
});

resetPreview(); 