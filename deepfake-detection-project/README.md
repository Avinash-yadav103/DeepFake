# 🛡️ Deepfake Detection System

Advanced deepfake detection using EfficientNet with Attention Mechanisms and Squeeze-and-Excitation blocks.

## 🌟 Features

- **AI-Powered Detection**: Uses state-of-the-art deep learning (EfficientNetB0 + CBAM + SE)
- **High Accuracy**: 95%+ accuracy on test data
- **Real-time Analysis**: Fast prediction in seconds
- **User-Friendly Interface**: Drag-and-drop image upload
- **Detailed Results**: Confidence scores, probability, and metrics
- **Face Detection**: Optional face detection validation
- **Responsive Design**: Works on desktop and mobile

## 🏗️ Architecture

**Model 4: Attention → EfficientNet → SE**

1. **Initial Attention Layer**: Enhanced CBAM for feature extraction
2. **EfficientNet Backbone**: Pre-trained on ImageNet, fine-tuned for deepfakes
3. **SE Blocks**: Channel-wise attention for important features
4. **Multi-layer Classifier**: Dense layers with regularization

## 📊 Performance

| Metric | Score |
|--------|-------|
| Accuracy | 95.2% |
| ROC AUC | 0.97 |
| Precision | 94.1% |
| Recall | 96.3% |
| F1-Score | 95.2% |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd deepfake-detection-project
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and set your configuration
```

5. **Ensure model weights are in place**
```
Place your trained model weights in the models/ directory:
- Model_4_Optimized_best.weights.h5
- Model_4_Optimized_best_loss.weights.h5
```

### Running the Application

#### Development Mode
```bash
python run.py
```

Visit http://localhost:5000 in your browser.

#### Production Mode
```bash
# Set environment
export FLASK_ENV=production  # Linux/Mac
set FLASK_ENV=production     # Windows

# Using gunicorn (Linux/Mac)
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

# Using waitress (Windows)
pip install waitress
waitress-serve --port=5000 --call app:create_app
```

## 📁 Project Structure

```
deepfake-detection-project/
│
├── app/
│   ├── __init__.py          # App factory
│   ├── routes.py            # Routes and endpoints
│   ├── models.py            # Model architecture and loading
│   └── utils.py             # Utility functions
│
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   ├── js/
│   │   └── main.js          # Frontend logic
│   └── uploads/             # Uploaded images
│
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   ├── result.html          # Results page
│   └── about.html           # About page
│
├── models/
│   └── *.weights.h5         # Trained model weights
│
├── notebooks/
│   ├── AvinashDeepFake.ipynb    # Initial experiments
│   ├── BestModel.ipynb          # Optimized model
│   ├── Commit1.ipynb            # First commit version
│   └── pretrainedmodeldeepfake.ipynb
│
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── NOTEBOOK_DOCUMENTATION.// filepath: README.md
# 🛡️ Deepfake Detection System

Advanced deepfake detection using EfficientNet with Attention Mechanisms and Squeeze-and-Excitation blocks.

## 🌟 Features

- **AI-Powered Detection**: Uses state-of-the-art deep learning (EfficientNetB0 + CBAM + SE)
- **High Accuracy**: 95%+ accuracy on test data
- **Real-time Analysis**: Fast prediction in seconds
- **User-Friendly Interface**: Drag-and-drop image upload
- **Detailed Results**: Confidence scores, probability, and metrics
- **Face Detection**: Optional face detection validation
- **Responsive Design**: Works on desktop and mobile

## 🏗️ Architecture

**Model 4: Attention → EfficientNet → SE**

1. **Initial Attention Layer**: Enhanced CBAM for feature extraction
2. **EfficientNet Backbone**: Pre-trained on ImageNet, fine-tuned for deepfakes
3. **SE Blocks**: Channel-wise attention for important features
4. **Multi-layer Classifier**: Dense layers with regularization

## 📊 Performance

| Metric | Score |
|--------|-------|
| Accuracy | 95.2% |
| ROC AUC | 0.97 |
| Precision | 94.1% |
| Recall | 96.3% |
| F1-Score | 95.2% |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd deepfake-detection-project
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and set your configuration
```

5. **Ensure model weights are in place**
```
Place your trained model weights in the models/ directory:
- Model_4_Optimized_best.weights.h5
- Model_4_Optimized_best_loss.weights.h5
```

### Running the Application

#### Development Mode
```bash
python run.py
```

Visit http://localhost:5000 in your browser.

#### Production Mode
```bash
# Set environment
export FLASK_ENV=production  # Linux/Mac
set FLASK_ENV=production     # Windows

# Using gunicorn (Linux/Mac)
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

# Using waitress (Windows)
pip install waitress
waitress-serve --port=5000 --call app:create_app
```

## 📁 Project Structure

```
deepfake-detection-project/
│
├── app/
│   ├── __init__.py          # App factory
│   ├── routes.py            # Routes and endpoints
│   ├── models.py            # Model architecture and loading
│   └── utils.py             # Utility functions
│
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   ├── js/
│   │   └── main.js          # Frontend logic
│   └── uploads/             # Uploaded images
│
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   ├── result.html          # Results page
│   └── about.html           # About page
│
├── models/
│   └── *.weights.h5         # Trained model weights
│
├── notebooks/
│   ├── AvinashDeepFake.ipynb    # Initial experiments
│   ├── BestModel.ipynb          # Optimized model
│   ├── Commit1.ipynb            # First commit version
│   └── pretrainedmodeldeepfake.ipynb
│
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── NOTEBOOK_DOCUMENTATION.