// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const previewSection = document.getElementById('previewSection');
const imagePreview = document.getElementById('imagePreview');
const analyzeBtn = document.getElementById('analyzeBtn');
const cancelBtn = document.getElementById('cancelBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorAlert = document.getElementById('errorAlert');
const errorMessage = document.getElementById('errorMessage');
const resultsSection = document.getElementById('resultsSection');

let selectedFile = null;

// Initialize drag and drop
if (uploadArea) {
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.classList.remove('dragover');
        }, false);
    });

    // Handle dropped files
    uploadArea.addEventListener('drop', handleDrop, false);
    uploadArea.addEventListener('click', () => imageInput.click());
}

// File input change handler
if (imageInput) {
    imageInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            handleFile(this.files[0]);
        }
    });
}

// Analyze button click handler
if (analyzeBtn) {
    analyzeBtn.addEventListener('click', analyzeImage);
}

// Cancel button click handler
if (cancelBtn) {
    cancelBtn.addEventListener('click', resetUpload);
}

// Functions
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;

    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFile(file) {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
        showError('Please upload a valid image file (JPG, JPEG, or PNG)');
        return;
    }

    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showError('File size must be less than 16MB');
        return;
    }

    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        uploadArea.style.display = 'none';
        previewSection.style.display = 'block';
        hideError();
    };
    reader.readAsDataURL(file);
}

function analyzeImage() {
    if (!selectedFile) {
        showError('No file selected');
        return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);

    // Show loading
    previewSection.style.display = 'none';
    loadingSpinner.style.display = 'block';
    hideError();

    // Send request
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.error || 'Prediction failed');
            });
        }
        return response.json();
    })
    .then(data => {
        loadingSpinner.style.display = 'none';
        displayResults(data);
    })
    .catch(error => {
        loadingSpinner.style.display = 'none';
        previewSection.style.display = 'block';
        showError(error.message);
    });
}

function displayResults(data) {
    // Hide previous sections
    uploadArea.style.display = 'none';
    previewSection.style.display = 'none';

    // Set result image
    document.getElementById('resultImage').src = data.image_url;

    // Set header color
    const header = document.getElementById('resultHeader');
    header.className = data.is_fake ? 'card-header text-white text-center py-3 fake' : 'card-header text-white text-center py-3 real';

    // Set prediction badge
    const badge = document.getElementById('predictionBadge');
    badge.textContent = data.prediction;
    badge.className = data.is_fake ? 'badge fake' : 'badge real';
    badge.style.backgroundColor = data.color;

    // Set confidence
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceText = document.getElementById('confidenceText');
    const confidenceLevel = document.getElementById('confidenceLevel');
    
    confidenceBar.style.width = data.confidence + '%';
    confidenceBar.style.backgroundColor = data.color;
    confidenceText.textContent = data.confidence.toFixed(2) + '%';
    confidenceLevel.textContent = data.confidence_level + ' Confidence';

    // Set probability
    document.getElementById('probabilityScore').textContent = data.probability.toFixed(4);

    // Set threshold
    document.getElementById('thresholdValue').textContent = data.threshold.toFixed(3);

    // Set face detection
    const faceDetected = document.getElementById('faceDetected');
    if (data.has_face) {
        faceDetected.innerHTML = '<span class="badge bg-success"><i class="fas fa-check"></i> Yes</span>';
    } else {
        faceDetected.innerHTML = '<span class="badge bg-warning"><i class="fas fa-question"></i> No</span>';
    }

    // Set image info
    if (data.image_info) {
        document.getElementById('imageFormat').textContent = data.image_info.format || 'Unknown';
        document.getElementById('imageSize').textContent = 
            `${data.image_info.width || 0} x ${data.image_info.height || 0}`;
    }

    // Show results
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function resetUpload() {
    selectedFile = null;
    imageInput.value = '';
    uploadArea.style.display = 'block';
    previewSection.style.display = 'none';
    resultsSection.style.display = 'none';
    hideError();
}

function showError(message) {
    errorMessage.textContent = message;
    errorAlert.style.display = 'block';
    errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function hideError() {
    errorAlert.style.display = 'none';
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    console.log('Deepfake Detection System Loaded');
});

$(document).ready(function() {
    const uploadArea = $('#upload-area');
    const fileInput = $('#file-input');
    const previewSection = $('#preview-section');
    const imagePreview = $('#image-preview');
    const submitBtn = $('#submit-btn');
    const uploadForm = $('#upload-form');
    const loading = $('#loading');
    const errorAlert = $('#error-alert');
    const errorMessage = $('#error-message');
    const resultSection = $('#result-section');
    const resultContent = $('#result-content');

    // Drag and drop functionality
    uploadArea.on('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass('dragover');
    });

    uploadArea.on('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragover');
    });

    uploadArea.on('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('dragover');
        
        const files = e.originalEvent.dataTransfer.files;
        if (files.length > 0) {
            fileInput[0].files = files;
            handleFileSelect(files[0]);
        }
    });

    // Click to upload
    uploadArea.on('click', function() {
        fileInput.click();
    });

    // File input change
    fileInput.on('change', function(e) {
        if (this.files && this.files[0]) {
            handleFileSelect(this.files[0]);
        }
    });

    // Remove image button
    $('#remove-image').on('click', function() {
        resetForm();
    });

    // Handle file selection
    function handleFileSelect(file) {
        // Validate file type
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        if (!validTypes.includes(file.type)) {
            showError('Invalid file type. Please upload JPG, JPEG, or PNG image.');
            return;
        }

        // Validate file size (16MB)
        if (file.size > 16 * 1024 * 1024) {
            showError('File too large. Maximum size is 16MB.');
            return;
        }

        // Preview image
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.attr('src', e.target.result);
            uploadArea.hide();
            previewSection.show().addClass('fade-in');
            submitBtn.prop('disabled', false);
            hideError();
        };
        reader.readAsDataURL(file);
    }

    // Form submission
    uploadForm.on('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        const file = fileInput[0].files[0];
        
        if (!file) {
            showError('Please select an image first.');
            return;
        }

        formData.append('file', file);

        // Show loading
        submitBtn.prop('disabled', true);
        loading.show().addClass('fade-in');
        hideError();
        resultSection.hide();

        // Make prediction request
        $.ajax({
            url: '/predict',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                displayResult(response);
            },
            error: function(xhr) {
                let message = 'An error occurred during prediction.';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    message = xhr.responseJSON.error;
                }
                showError(message);
                submitBtn.prop('disabled', false);
            },
            complete: function() {
                loading.hide();
            }
        });
    });

    // Display prediction result
    function displayResult(data) {
        const isFake = data.prediction === 'FAKE';
        const confidence = data.confidence.toFixed(2);
        const probability = data.probability.toFixed(2);

        const resultHTML = `
            <div class="result-card ${isFake ? 'fake' : 'real'} fade-in">
                <div class="result-icon pulse">
                    <i class="fas fa-${isFake ? 'exclamation-triangle' : 'check-circle'}"></i>
                </div>
                <h2 class="mb-3">
                    ${isFake ? '⚠️ DEEPFAKE DETECTED' : '✅ REAL IMAGE'}
                </h2>
                <p class="lead mb-4">
                    The image is classified as <strong>${data.prediction}</strong>
                </p>
                
                <div class="confidence-bar">
                    <div class="confidence-fill ${isFake ? 'fake' : 'real'}" 
                         style="width: ${confidence}%;">
                        ${confidence}%
                    </div>
                </div>
                
                <div class="mt-4">
                    <h5>Analysis Details:</h5>
                    <div class="row mt-3 text-start">
                        <div class="col-md-6">
                            <p><strong>Confidence:</strong> ${confidence}%</p>
                            <p><strong>Fake Probability:</strong> ${probability}%</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Model Threshold:</strong> ${(data.threshold * 100).toFixed(1)}%</p>
                            <p><strong>Upload Time:</strong> ${data.upload_time}</p>
                        </div>
                    </div>
                </div>

                <div class="alert ${isFake ? 'alert-light' : 'alert-light'} mt-4 text-dark">
                    <i class="fas fa-info-circle me-2"></i>
                    ${isFake 
                        ? '<strong>Warning:</strong> This image appears to be AI-generated or manipulated. Exercise caution when sharing or using this content.'
                        : '<strong>Note:</strong> This image appears to be authentic. However, always verify the source of important media content.'
                    }
                </div>
            </div>
        `;

        resultContent.html(resultHTML);
        resultSection.show().addClass('fade-in');

        // Smooth scroll to result
        $('html, body').animate({
            scrollTop: resultSection.offset().top - 100
        }, 500);
    }

    // Show error message
    function showError(message) {
        errorMessage.text(message);
        errorAlert.show().addClass('fade-in');
    }

    // Hide error message
    function hideError() {
        errorAlert.hide().removeClass('fade-in');
    }

    // Reset form
    function resetForm() {
        fileInput.val('');
        previewSection.hide();
        uploadArea.show();
        submitBtn.prop('disabled', true);
        resultSection.hide();
        hideError();
    }

    // Initialize
    console.log('🚀 Deepfake Detector initialized!');
});