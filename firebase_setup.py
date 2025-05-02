import firebase_admin
from firebase_admin import credentials, firestore

# Firebase initialization (safe for Streamlit reruns)
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
