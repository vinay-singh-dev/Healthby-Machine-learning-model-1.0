from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model
import os
import sys

# Load the trained model
try:
    model = load_model("fine_tuned_skin_model.h5")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    sys.exit(1)

# Define top 10 classes (must match the classes used during training)
top_10_classes = [
    "Benign Tumors", "Eczema", "Tinea", "Psoriasis",
    "Actinic Keratosis", "Vitiligo", "Skin Cancer", "Warts", "Acne"
]

# Image path (update this path or pass it as a command-line argument)
img_path = r"C:\Users\Vinay Singh Baghel\OneDrive\Desktop\AI_Health_Tracker\images\OIP.jpeg"

# Check if image file exists
if not os.path.exists(img_path):
    print(f"❌ Image file not found at: {img_path}")
    sys.exit(1)

# Load and preprocess the image
try:
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
except Exception as e:
    print(f"❌ Error processing image: {e}")
    sys.exit(1)

# Predict the class
try:
    prediction = model.predict(img_array)
    predicted_class = top_10_classes[np.argmax(prediction)]
    confidence = np.max(prediction)
    print(f"✅ Predicted Class: {predicted_class} ({confidence * 100:.2f}%)")
except Exception as e:
    print(f"❌ Error during prediction: {e}")
