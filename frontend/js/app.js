const form = document.getElementById('predict-form');
const fileInput = document.getElementById('image-input');
const resultBox = document.getElementById('result');
const uploadedImage = document.getElementById('uploaded-image');
const produceName = document.getElementById('produce-name');
const freshnessValue = document.getElementById('freshness-value');
const confidenceValue = document.getElementById('confidence-value');
const messageBox = document.getElementById('message-box');
const cameraButton = document.getElementById('camera-button');
const cameraContainer = document.getElementById('camera-container');
const captureButton = document.getElementById('capture-button');
const retakeButton = document.getElementById('retake-button');
const video = document.getElementById('camera-preview');

let stream = null;
let capturedImageData = null;

async function openCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    video.srcObject = stream;
    cameraContainer.classList.remove('hidden');
  } catch (error) {
    messageBox.textContent = 'Camera access was denied or is unavailable. Please upload an image instead.';
    messageBox.style.color = '#dc2626';
  }
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
    stream = null;
  }
  cameraContainer.classList.add('hidden');
}

async function handlePrediction(event) {
  event.preventDefault();

  const file = fileInput.files[0] || capturedImageData;
  if (!file) {
    messageBox.textContent = 'Please choose an image or capture one first.';
    messageBox.style.color = '#dc2626';
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  messageBox.textContent = 'Analyzing image...';
  messageBox.style.color = '#1f6feb';

  try {
    const response = await fetch('http://localhost:8000/api/predict', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Prediction failed.');
    }

    resultBox.classList.remove('hidden');
    uploadedImage.src = URL.createObjectURL(file);
    produceName.textContent = data.produce || 'Unknown';
    freshnessValue.textContent = data.freshness || 'Unknown';
    confidenceValue.textContent = `${((data.confidence || 0) * 100).toFixed(1)}%`;
    messageBox.textContent = data.message || 'Prediction completed.';
    messageBox.style.color = '#1a2433';
    stopCamera();
  } catch (error) {
    messageBox.textContent = error.message || 'Prediction failed.';
    messageBox.style.color = '#dc2626';
  }
}

cameraButton.addEventListener('click', openCamera);
captureButton.addEventListener('click', () => {
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');
  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 480;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.toBlob((blob) => {
    capturedImageData = new File([blob], 'camera-capture.png', { type: 'image/png' });
    fileInput.files = new DataTransfer().files;
    resultBox.classList.remove('hidden');
    uploadedImage.src = URL.createObjectURL(capturedImageData);
    stopCamera();
  }, 'image/png');
});

retakeButton.addEventListener('click', () => {
  stopCamera();
  openCamera();
});

form.addEventListener('submit', handlePrediction);
