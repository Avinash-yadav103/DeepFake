from flask import Flask
import os
from config import config

def create_app(config_name=None):
    """Application factory pattern"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create Flask app with correct template and static folders
    app = Flask(__name__, 
                template_folder='../templates',  # Point to templates folder
                static_folder='../static')       # Point to static folder
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Register routes
    from app import routes
    app.register_blueprint(routes.bp)
    
    return app
