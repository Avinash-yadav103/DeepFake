import os
import cv2
import numpy as np
from datetime import datetime
from flask import current_app

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_size(filepath):
    """Get file size in bytes"""
    return os.path.getsize(filepath)

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_name = ["B", "KB", "MB", "GB"]
    i = int(np.floor(np.log(size_bytes) / np.log(1024)))
    p = np.power(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def preprocess_image(image_path, target_size=(224, 224)):
    """Preprocess image for model prediction"""
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image file")
        
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize image
        image = cv2.resize(image, target_size)
        
        # Normalize to [0, 1]
        image = image.astype(np.float32) / 255.0
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        
        return image
    
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {str(e)}")

def load_model(model_path):
    """Load the trained model"""
    try:
        # Import TensorFlow only when needed
        import tensorflow as tf
        from tensorflow import keras
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load model weights
        model = create_model()
        model.load_weights(model_path)
        
        return model
    
    except ImportError:
        raise ImportError("TensorFlow is required for model loading. Please install it with: pip install tensorflow")
    except Exception as e:
        raise ValueError(f"Error loading model: {str(e)}")

def create_model():
    """Create the model architecture"""
    try:
        # Import TensorFlow only when needed
        import tensorflow as tf
        from tensorflow import keras
        
        # This is a basic model structure - adjust based on your actual model
        model = keras.Sequential([
            keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Conv2D(128, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            keras.layers.Flatten(),
            keras.layers.Dense(512, activation='relu'),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    except ImportError:
        raise ImportError("TensorFlow is required for model creation. Please install it with: pip install tensorflow")

def make_prediction(model, image_path, threshold=0.5):
    """Make prediction on an image"""
    try:
        # Preprocess image
        processed_image = preprocess_image(image_path)
        
        # Make prediction
        prediction = model.predict(processed_image)[0][0]
        
        # Determine result
        is_fake = prediction > threshold
        confidence = float(prediction if is_fake else 1 - prediction)
        
        return {
            'prediction': float(prediction),
            'is_fake': is_fake,
            'confidence': confidence,
            'label': 'Fake' if is_fake else 'Real'
        }
    
    except Exception as e:
        raise ValueError(f"Error making prediction: {str(e)}")

class DeepfakeDetector:
    """Singleton class for deepfake detection"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = None
            cls._instance.threshold = 0.5
            cls._instance.is_loaded = False
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def load_model(self, model_path, threshold=0.5):
        """Load the model"""
        try:
            self.model = load_model(model_path)
            self.threshold = threshold
            self.is_loaded = True
        except Exception as e:
            self.is_loaded = False
            raise e
    
    def predict(self, image_path):
        """Make prediction on image"""
        if not self.is_loaded or self.model is None:
            raise ValueError("Model not loaded")
        
        return make_prediction(self.model, image_path, self.threshold)