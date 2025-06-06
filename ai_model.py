import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# model loading 
try:
    model = load_model("fine_tuned_skin_model.h5")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None  # Set to None to avoid crash if model fails to load

# disease classess for model training
class_indices = {
    0: 'Benign Tumors',
    1: 'Eczema',
    2: 'Tinea',
    3: 'Psoriasis',
    4: 'Actinic Keratosis',
    5: 'Vitiligo',
    6: 'Skin Cancer',
    7: 'Warts',
    8: 'Acne'
}

def diagnose_image(img_path):
    if model is None:
        return "Model not loaded. Please check the model file."

    if not os.path.exists(img_path):
        return f"❌ Image file not found: {img_path}"

    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)[0]
        predicted_index = np.argmax(prediction)
        predicted_class = class_indices.get(predicted_index, "Unknown")
        confidence = prediction[predicted_index] * 100

        return f"{predicted_class} ({confidence:.2f}% confidence)"
    
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return "Prediction failed. Please try again."
