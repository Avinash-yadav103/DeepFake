import os
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
import cv2

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Preprocess image for model prediction
    
    Args:
        image_path: Path to the image file
        target_size: Target size for resizing (width, height)
    
    Returns:
        Preprocessed image as numpy array with shape (224, 224, 3) and values in [0, 1]
    """
    try:
        # Load image using PIL
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize image
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img, dtype=np.float32)
        
        # Normalize to [0, 1]
        img_array = img_array / 255.0
        
        return img_array
        
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {str(e)}")

def get_image_info(image_path):
    """Get information about the image"""
    try:
        img = Image.open(image_path)
        return {
            'format': img.format,
            'mode': img.mode,
            'size': img.size,
            'width': img.width,
            'height': img.height
        }
    except Exception as e:
        return {'error': str(e)}

def detect_face(image_path):
    """
    Detect face in image using OpenCV Haar Cascade
    Returns True if face detected, False otherwise
    """
    try:
        # Load the cascade
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Read the image
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        return len(faces) > 0
        
    except Exception as e:
        print(f"Face detection error: {str(e)}")
        return True  # Assume face present if detection fails

def save_uploaded_file(file, upload_folder):
    """
    Save uploaded file to the upload folder
    
    Args:
        file: FileStorage object from request.files
        upload_folder: Path to upload folder
    
    Returns:
        Path to saved file
    """
    filename = secure_filename(file.filename)
    
    # Add timestamp to filename to avoid conflicts
    import time
    timestamp = str(int(time.time()))
    name, ext = os.path.splitext(filename)
    filename = f"{name}_{timestamp}{ext}"
    
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    
    return filepath

def cleanup_old_uploads(upload_folder, max_age_seconds=3600):
    """
    Clean up old uploaded files
    
    Args:
        upload_folder: Path to upload folder
        max_age_seconds: Maximum age of files in seconds (default 1 hour)
    """
    import time
    
    try:
        current_time = time.time()
        
        for filename in os.listdir(upload_folder):
            if filename == '.gitkeep':
                continue
                
            filepath = os.path.join(upload_folder, filename)
            
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                
                if file_age > max_age_seconds:
                    os.remove(filepath)
                    print(f"Removed old file: {filename}")
                    
    except Exception as e:
        print(f"Cleanup error: {str(e)}")

def get_confidence_level(confidence):
    """
    Get confidence level description
    
    Args:
        confidence: Confidence percentage (0-100)
    
    Returns:
        Confidence level description
    """
    if confidence >= 95:
        return "Very High"
    elif confidence >= 85:
        return "High"
    elif confidence >= 70:
        return "Moderate"
    elif confidence >= 60:
        return "Low"
    else:
        return "Very Low"

def get_prediction_color(is_fake, confidence):
    """
    Get color for prediction based on result and confidence
    
    Returns:
        Color code for UI
    """
    if is_fake:
        if confidence >= 85:
            return "#dc3545"  # Red - High confidence fake
        else:
            return "#fd7e14"  # Orange - Low confidence fake
    else:
        if confidence >= 85:
            return "#28a745"  # Green - High confidence real
        else:
            return "#ffc107"  # Yellow - Low confidence real

def get_file_size(filepath):
    """Get file size in bytes"""
    return os.path.getsize(filepath)

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def validate_image(filepath):
    """Validate if file is a valid image"""
    try:
        img = Image.open(filepath)
        img.verify()
        return True
    except:
        return False

def get_image_dimensions(filepath):
    """Get image dimensions"""
    try:
        img = Image.open(filepath)
        return img.size
    except:
        return None, None