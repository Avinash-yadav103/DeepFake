from flask import Flask
import os

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    from config import config as config_dict
    app.config.from_object(config_dict[config_name])
    config_dict[config_name].init_app(app)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Initialize model on startup
    from app.models import DeepfakeDetector
    with app.app_context():
        try:
            detector = DeepfakeDetector.get_instance()
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"⚠️ Warning: Could not load model on startup: {str(e)}")
            print("Model will be loaded on first prediction request.")
    
    return app
