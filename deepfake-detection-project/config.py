import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    
    # File Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = set(os.environ.get('ALLOWED_EXTENSIONS', 'jpg,jpeg,png').split(','))
    
    # Model Configuration
    MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                             os.environ.get('MODEL_PATH', 'models/Model_4_Optimized_best.weights.h5'))
    MODEL_INPUT_SIZE = (224, 224)
    
    # Prediction Thresholds
    OPTIMAL_THRESHOLD = 0.5
    CONFIDENCE_THRESHOLD = 0.3
    
    # Session
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600
    
    @staticmethod
    def init_app(app):
        """Initialize application configuration"""
        # Create upload folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Require SECRET_KEY in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        # For now, use a default for easier deployment
        SECRET_KEY = 'production-secret-key-change-this-in-deployment'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}