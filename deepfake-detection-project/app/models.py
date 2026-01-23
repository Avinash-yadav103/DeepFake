import numpy as np
from PIL import Image
import os
import warnings
warnings.filterwarnings('ignore')

# Lazy import TensorFlow to avoid startup issues
tf = None
Model = None
Input = None
Conv2D = None
BatchNormalization = None
Add = None
Dense = None
GlobalAveragePooling2D = None
GlobalMaxPooling2D = None
Concatenate = None
Dropout = None
Multiply = None
Reshape = None
Lambda = None
Activation = None
EfficientNetB0 = None
l2 = None

def _import_tensorflow():
    """Lazy import TensorFlow components"""
    global tf, Model, Input, Conv2D, BatchNormalization, Add, Dense
    global GlobalAveragePooling2D, GlobalMaxPooling2D, Concatenate
    global Dropout, Multiply, Reshape, Lambda, Activation, EfficientNetB0, l2
    
    try:
        import tensorflow as tf_module
        from tensorflow.keras.models import Model as ModelClass
        from tensorflow.keras.layers import (Input as InputLayer, Conv2D as Conv2DLayer, 
                                           BatchNormalization as BNLayer, Add as AddLayer, 
                                           Dense as DenseLayer, GlobalAveragePooling2D as GAPLayer, 
                                           GlobalMaxPooling2D as GMPLayer, Concatenate as ConcatLayer, 
                                           Dropout as DropoutLayer, Multiply as MultiplyLayer, 
                                           Reshape as ReshapeLayer, Lambda as LambdaLayer, 
                                           Activation as ActivationLayer)
        from tensorflow.keras.applications import EfficientNetB0 as EfficientNet
        from tensorflow.keras.regularizers import l2 as l2_reg
        
        tf = tf_module
        Model = ModelClass
        Input = InputLayer
        Conv2D = Conv2DLayer
        BatchNormalization = BNLayer
        Add = AddLayer
        Dense = DenseLayer
        GlobalAveragePooling2D = GAPLayer
        GlobalMaxPooling2D = GMPLayer
        Concatenate = ConcatLayer
        Dropout = DropoutLayer
        Multiply = MultiplyLayer
        Reshape = ReshapeLayer
        Lambda = LambdaLayer
        Activation = ActivationLayer
        EfficientNetB0 = EfficientNet
        l2 = l2_reg
        
        return True
    except Exception as e:
        print(f"⚠️ TensorFlow import failed: {e}")
        return False


class DeepfakeDetector:
    """Singleton class for deepfake detection model"""
    
    _instance = None
    _model = None
    
    def __init__(self):
        """Initialize the detector"""
        if DeepfakeDetector._model is None:
            self.model = None
            self.optimal_threshold = 0.5
            self.is_loaded = False
    
    @classmethod
    def get_instance(cls):
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @staticmethod
    def enhanced_se_block(input_feature, ratio=16, name="se_block"):
        """Enhanced Squeeze-and-Excitation block"""
        channel = input_feature.shape[-1]
        
        avg_pool = GlobalAveragePooling2D(name=f'{name}_avg_pool')(input_feature)
        max_pool = GlobalMaxPooling2D(name=f'{name}_max_pool')(input_feature)
        
        avg_pool = Reshape((1, 1, channel), name=f'{name}_avg_reshape')(avg_pool)
        max_pool = Reshape((1, 1, channel), name=f'{name}_max_reshape')(max_pool)
        
        avg_excite = Dense(channel // ratio, activation='relu', 
                          kernel_regularizer=l2(1e-4), name=f'{name}_avg_dense1')(avg_pool)
        avg_excite = Dropout(0.1, name=f'{name}_avg_dropout')(avg_excite)
        avg_excite = Dense(channel, activation='sigmoid', name=f'{name}_avg_dense2')(avg_excite)
        
        max_excite = Dense(channel // ratio, activation='relu',
                          kernel_regularizer=l2(1e-4), name=f'{name}_max_dense1')(max_pool)
        max_excite = Dropout(0.1, name=f'{name}_max_dropout')(max_excite)
        max_excite = Dense(channel, activation='sigmoid', name=f'{name}_max_dense2')(max_excite)
        
        se_feature = Add(name=f'{name}_add')([avg_excite, max_excite])
        feature = Multiply(name=f'{name}_multiply')([input_feature, se_feature])
        
        return feature
    
    @staticmethod
    def enhanced_cbam_block(input_feature, ratio=16, name="cbam_block"):
        """Enhanced CBAM (Convolutional Block Attention Module)"""
        channel = input_feature.shape[-1]
        
        # Channel Attention
        avg_pool = GlobalAveragePooling2D(keepdims=True, name=f'{name}_ch_avg')(input_feature)
        max_pool = GlobalMaxPooling2D(keepdims=True, name=f'{name}_ch_max')(input_feature)
        
        avg_pool = Dense(channel // ratio, activation='relu', name=f'{name}_ch_dense1_avg')(avg_pool)
        avg_pool = Dropout(0.1, name=f'{name}_ch_dropout_avg')(avg_pool)
        avg_pool = Dense(channel, name=f'{name}_ch_dense2_avg')(avg_pool)
        
        max_pool = Dense(channel // ratio, activation='relu', name=f'{name}_ch_dense1_max')(max_pool)
        max_pool = Dropout(0.1, name=f'{name}_ch_dropout_max')(max_pool)
        max_pool = Dense(channel, name=f'{name}_ch_dense2_max')(max_pool)
        
        channel_attention = Add(name=f'{name}_ch_add')([avg_pool, max_pool])
        channel_attention = Activation('sigmoid', name=f'{name}_ch_sigmoid')(channel_attention)
        feature = Multiply(name=f'{name}_ch_multiply')([input_feature, channel_attention])
        
        # Spatial Attention
        avg_pool_spatial = Lambda(lambda x: tf.reduce_mean(x, axis=3, keepdims=True), 
                                 name=f'{name}_sp_avg')(feature)
        max_pool_spatial = Lambda(lambda x: tf.reduce_max(x, axis=3, keepdims=True), 
                                 name=f'{name}_sp_max')(feature)
        
        spatial_attention = Concatenate(axis=3, name=f'{name}_sp_concat')([avg_pool_spatial, max_pool_spatial])
        spatial_attention = Conv2D(1, (7, 7), strides=1, padding='same', activation='sigmoid',
                                  kernel_regularizer=l2(1e-4), name=f'{name}_sp_conv')(spatial_attention)
        
        feature = Multiply(name=f'{name}_sp_multiply')([feature, spatial_attention])
        
        return feature
    
    def build_model_architecture(self, input_shape=(224, 224, 3)):
        """Build the optimized Model 4 architecture"""
        print("🏗️ Building model architecture...")
        
        # Ensure TensorFlow is imported
        if not _import_tensorflow():
            raise RuntimeError("TensorFlow not available")
        
        inputs = Input(shape=input_shape, name='input_layer')
        
        # Stage 1: Initial Processing with Attention
        x = Conv2D(32, 3, padding='same', activation='relu', 
                  kernel_regularizer=l2(1e-4), name='initial_conv1')(inputs)
        x = BatchNormalization(name='initial_bn1')(x)
        
        x = Conv2D(64, 3, padding='same', activation='relu',
                  kernel_regularizer=l2(1e-4), name='initial_conv2')(x)
        x = BatchNormalization(name='initial_bn2')(x)
        
        attention_out = self.enhanced_cbam_block(x, ratio=16, name='initial_cbam')
        
        if x.shape[-1] == attention_out.shape[-1]:
            x = Add(name='initial_residual')([x, attention_out])
        else:
            projected = Conv2D(attention_out.shape[-1], 1, padding='same', name='initial_project')(x)
            x = Add(name='initial_residual')([projected, attention_out])
        
        # Stage 2: Prepare for EfficientNet
        x = Lambda(lambda x: tf.image.resize(x, [224, 224]), name='resize_for_efficientnet')(x)
        x = Conv2D(3, 1, padding='same', activation='linear', name='channel_adjust')(x)
        
        # Stage 3: EfficientNet Backbone
        base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=input_shape)
        base_model.trainable = True
        for layer in base_model.layers[:-30]:
            layer.trainable = False
        
        efficientnet_out = base_model(x)
        
        # Stage 4: SE Module
        se_out = self.enhanced_se_block(efficientnet_out, ratio=16, name='final_se')
        
        # Stage 5: Classifier Head
        x = GlobalAveragePooling2D(name='global_avg_pool')(se_out)
        x_max = GlobalMaxPooling2D(name='global_max_pool')(se_out)
        x = Concatenate(name='pool_concat')([x, x_max])
        
        x = Dense(1024, activation='relu', kernel_regularizer=l2(1e-3), name='classifier_dense1')(x)
        x = BatchNormalization(name='classifier_bn1')(x)
        x = Dropout(0.5, name='classifier_dropout1')(x)
        
        x = Dense(512, activation='relu', kernel_regularizer=l2(1e-3), name='classifier_dense2')(x)
        x = BatchNormalization(name='classifier_bn2')(x)
        x = Dropout(0.4, name='classifier_dropout2')(x)
        
        x = Dense(256, activation='relu', kernel_regularizer=l2(1e-3), name='classifier_dense3')(x)
        x = BatchNormalization(name='classifier_bn3')(x)
        x = Dropout(0.3, name='classifier_dropout3')(x)
        
        outputs = Dense(1, activation='sigmoid', name='output')(x)
        
        model = Model(inputs, outputs, name='Optimized_Attention_EfficientNet_SE')
        return model
    
    def load_model(self, model_path, optimal_threshold=0.5):
        """Load the trained model weights"""
        try:
            print(f"📂 Loading model from: {model_path}")
            
            # Import TensorFlow components
            if not _import_tensorflow():
                print("⚠️ TensorFlow not available - using demo mode")
                self.is_loaded = False
                return False
            
            if not os.path.exists(model_path):
                print(f"⚠️ Model file not found: {model_path}")
                self.is_loaded = False
                return False
            
            # Build model architecture
            print("🏗️ Building model architecture...")
            self.model = self.build_model_architecture()
            
            # Load weights
            print("⚙️ Loading weights...")
            self.model.load_weights(model_path)
            
            self.optimal_threshold = optimal_threshold
            self.is_loaded = True
            
            print(f"✅ Model loaded successfully!")
            print(f"   - Parameters: {self.model.count_params():,}")
            print(f"   - Optimal threshold: {self.optimal_threshold}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            import traceback
            print(traceback.format_exc())
            self.is_loaded = False
            return False
    
    def preprocess_image(self, image_path, target_size=(224, 224)):
        """Preprocess image for prediction"""
        try:
            # Load image
            img = Image.open(image_path).convert('RGB')
            
            # Resize
            img = img.resize(target_size, Image.LANCZOS)
            
            # Convert to array and normalize
            img_array = np.array(img, dtype=np.float32)
            img_array = img_array / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            raise ValueError(f"Error preprocessing image: {str(e)}")
    
    def predict(self, image_path):
        """Predict if image is fake or real"""
        # Check if TensorFlow is available
        if not _import_tensorflow():
            return self._demo_prediction(image_path)
        
        if not self.is_loaded or self.model is None:
            # Try to load model first
            try:
                from flask import current_app
                model_path = current_app.config.get('MODEL_PATH')
                if model_path and os.path.exists(model_path):
                    self.load_model(model_path)
                else:
                    return self._demo_prediction(image_path)
            except:
                return self._demo_prediction(image_path)
        
        try:
            # Preprocess image
            img_array = self.preprocess_image(image_path)
            
            # Make prediction
            prediction_prob = float(self.model.predict(img_array, verbose=0)[0][0])
            
            # Classify based on optimal threshold
            is_fake = prediction_prob > self.optimal_threshold
            
            # Calculate confidence
            confidence = prediction_prob if is_fake else (1 - prediction_prob)
            
            result = {
                'prediction': 'FAKE' if is_fake else 'REAL',
                'confidence': float(confidence * 100),
                'probability': float(prediction_prob * 100),
                'is_fake': bool(is_fake),
                'threshold': float(self.optimal_threshold),
                'model_used': 'DeepLearning'
            }
            
            return result
            
        except Exception as e:
            print(f"⚠️ Prediction error: {e}")
            return self._demo_prediction(image_path)
    
    def _demo_prediction(self, image_path):
        """Demo prediction when model is not available"""
        import random
        import hashlib
        
        # Use image hash for consistent demo results
        with open(image_path, 'rb') as f:
            image_hash = hashlib.md5(f.read()).hexdigest()
        
        # Generate pseudo-random but consistent result
        random.seed(image_hash)
        prediction_prob = random.uniform(0.1, 0.9)
        
        is_fake = prediction_prob > 0.5
        confidence = prediction_prob if is_fake else (1 - prediction_prob)
        
        result = {
            'prediction': 'FAKE' if is_fake else 'REAL',
            'confidence': float(confidence * 100),
            'probability': float(prediction_prob * 100),
            'is_fake': bool(is_fake),
            'threshold': 0.5,
            'model_used': 'Demo'
        }
        
        print(f"⚠️ Using demo prediction (model not available): {result['prediction']}")
        return result