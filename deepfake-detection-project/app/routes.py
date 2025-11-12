from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
import os
import cv2
import numpy as np
from datetime import datetime
from werkzeug.utils import secure_filename
from app.utils import allowed_file, DeepfakeDetector, get_file_size, format_file_size

# Create blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@bp.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            return jsonify({
                'error': f'Invalid file type. Allowed types: {", ".join(current_app.config["ALLOWED_EXTENSIONS"])}'
            }), 400
        
        # Save file
        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Check file size
        file_size = get_file_size(filepath)
        if file_size > current_app.config['MAX_FILE_SIZE']:
            os.remove(filepath)
            return jsonify({
                'error': f'File too large. Maximum size: {format_file_size(current_app.config["MAX_FILE_SIZE"])}'
            }), 400
        
        # Load model and predict
        detector = DeepfakeDetector.get_instance()
        
        if not detector.is_loaded:
            detector.load_model(
                current_app.config['MODEL_PATH'],
                current_app.config.get('OPTIMAL_THRESHOLD', 0.5)
            )
        
        # Make prediction
        result = detector.predict(filepath)
        
        # Add file info to result
        result['filename'] = filename
        result['file_size'] = format_file_size(file_size)
        result['upload_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify(result), 200
        
    except Exception as e:
        # Clean up file if it exists
        if 'filepath' in locals() and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        
        return jsonify({'error': str(e)}), 500

@bp.route('/result')
def result():
    """Result page"""
    return render_template('result.html')

@bp.route('/health')
def health():
    """Health check endpoint"""
    detector = DeepfakeDetector.get_instance()
    
    return jsonify({
        'status': 'healthy',
        'model_loaded': detector.is_loaded,
        'timestamp': datetime.now().isoformat()
    }), 200

@bp.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('index.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500