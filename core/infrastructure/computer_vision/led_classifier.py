import tensorflow as tf
from tensorflow.keras import layers, models
import cv2
import numpy as np
import os

class LEDClassifier:
    def __init__(self, model_path=None):
        if model_path and os.path.exists(model_path):
            self.model = tf.keras.models.load_model(model_path)
        else:
            self.model = self.build_model()
    
    def build_model(self):
        model = models.Sequential([
            layers.Rescaling(1./255, input_shape=(128, 128, 3)),
            layers.Conv2D(32, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        return model
    
    def preprocess_image(self, image_path):
        img = cv2.imread(image_path)
        img = cv2.resize(img, (128, 128))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return np.expand_dims(img, axis=0)
    
    def predict(self, image_path):
        processed_img = self.preprocess_image(image_path)
        prediction = self.model.predict(processed_img)
        return prediction[0][0] > 0.5  # Retorna True se LED
    
    def train(self, dataset_dir, epochs=10):
        train_ds = tf.keras.utils.image_dataset_from_directory(
            dataset_dir,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(128, 128),
            batch_size=32
        )
        
        val_ds = tf.keras.utils.image_dataset_from_directory(
            dataset_dir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(128, 128),
            batch_size=32
        )
        
        self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs
        )
        
        self.model.save('models/led_classifier.h5')