### Project Structure

```
deepfake_detection/
│
├── app.py                  # Main Flask application
├── model.py                # Model loading and prediction logic
├── static/                 # Static files (CSS, JS, images)
│   └── style.css           # CSS for styling
├── templates/              # HTML templates
│   └── index.html          # Main page for image upload
├── weights/                # Directory for model weights
│   └── model_weights.h5    # Pre-trained model weights
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

### Step 1: Setting Up the Flask Application

#### `app.py`

```python
from flask import Flask, request, render_template
from model import load_model, predict
import os

app = Flask(__name__)

# Load the pre-trained model
model = load_model('weights/model_weights.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        # Save the uploaded file
        file_path = os.path.join('static/uploads', file.filename)
        file.save(file_path)
        
        # Make prediction
        result = predict(model, file_path)
        
        return render_template('index.html', prediction=result)

if __name__ == '__main__':
    app.run(debug=True)
```

### Step 2: Model Loading and Prediction Logic

#### `model.py`

```python
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

def load_model(model_path):
    """Load the pre-trained model from the specified path."""
    model = tf.keras.models.load_model(model_path)
    return model

def preprocess_image(img_path):
    """Preprocess the image for prediction."""
    img = image.load_img(img_path, target_size=(224, 224))  # Adjust size as needed
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize
    return img_array

def predict(model, img_path):
    """Make a prediction on the uploaded image."""
    processed_image = preprocess_image(img_path)
    prediction = model.predict(processed_image)
    return "Deepfake" if prediction[0][0] > 0.5 else "Real"
```

### Step 3: Creating the User Interface

#### `templates/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <title>Deepfake Detection</title>
</head>
<body>
    <h1>Deepfake Detection</h1>
    <form action="/predict" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="image/*" required>
        <button type="submit">Upload and Predict</button>
    </form>
    {% if prediction %}
        <h2>Prediction: {{ prediction }}</h2>
    {% endif %}
</body>
</html>
```

### Step 4: Adding CSS for Styling

#### `static/style.css`

```css
body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin: 50px;
}

h1 {
    color: #333;
}

form {
    margin: 20px 0;
}

input[type="file"] {
    margin: 10px;
}

button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
```

### Step 5: Requirements File

#### `requirements.txt`

```
Flask==2.0.1
tensorflow==2.6.0
numpy==1.19.5
Pillow==8.4.0
```

### Step 6: Documentation

#### `README.md`

```markdown
# Deepfake Detection Flask Application

This project is a Flask web application for detecting deepfake images using a pre-trained deep learning model.

## Project Structure

- `app.py`: Main Flask application file.
- `model.py`: Contains functions for loading the model and making predictions.
- `static/`: Directory for static files (CSS, JS, images).
- `templates/`: Directory for HTML templates.
- `weights/`: Directory containing the pre-trained model weights.
- `requirements.txt`: List of Python dependencies.
- `README.md`: Project documentation.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd deepfake_detection
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Place your pre-trained model weights in the `weights/` directory and rename it to `model_weights.h5`.

## Running the Application

To run the application, execute the following command:

```bash
python app.py
```

Visit `http://127.0.0.1:5000/` in your web browser to access the application.

## Usage

1. Upload an image using the provided form.
2. Click on the "Upload and Predict" button.
3. The application will display whether the image is a "Deepfake" or "Real".

## License

This project is licensed under the MIT License.
```

### Conclusion

This guide provides a comprehensive overview of creating a Flask application for deepfake detection, including the necessary code and documentation. You can expand upon this foundation by adding features such as user authentication, logging, or more advanced model evaluation metrics.