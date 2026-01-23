from flask import Blueprint, render_template, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from app.models import DeepfakeDetector
from app.utils import allowed_file, get_image_info, detect_face
import traceback

bp = Blueprint('main', __name__)

# Initialize detector as singleton
detector = None

def get_detector():
    """Get or initialize the detector"""
    global detector
    if detector is None:
        detector = DeepfakeDetector.get_instance()
        # Load model on first request
        model_path = current_app.config.get('MODEL_PATH')
        if model_path and os.path.exists(model_path):
            try:
                detector.load_model(model_path, current_app.config.get('OPTIMAL_THRESHOLD', 0.5))
                print(f"✅ Model loaded from {model_path}")
            except Exception as e:
                print(f"⚠️ Could not load model: {e}")
                print("   Will use demo mode")
    return detector

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
    """Predict if uploaded image is fake or real"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload JPG, JPEG, or PNG'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get detector and make prediction
        model = get_detector()
        result = model.predict(filepath)
        
        # Get additional info
        image_info = get_image_info(filepath)
        has_face = detect_face(filepath)
        
        # Determine color based on prediction
        if result['is_fake']:
            color = '#dc3545'  # Red for fake
            confidence_level = 'High' if result['confidence'] > 70 else 'Medium'
        else:
            color = '#28a745'  # Green for real
            confidence_level = 'High' if result['confidence'] > 70 else 'Medium'
        
        # Prepare response
        response = {
            'success': True,
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'probability': result['probability'],
            'is_fake': result['is_fake'],
            'threshold': result['threshold'],
            'model_used': result.get('model_used', 'DeepLearning'),
            'confidence_level': confidence_level,
            'color': color,
            'has_face': has_face,
            'image_info': image_info,
            'image_url': f'/static/uploads/{filename}'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Prediction error: {error_msg}")
        print(traceback.format_exc())
        return jsonify({'error': f'Prediction failed: {error_msg}'}), 500

@bp.route('/health')
def health():
    """Health check endpoint"""
    model = get_detector()
    return jsonify({
        'status': 'healthy',
        'model_loaded': model.is_loaded if model else False
    }), 200