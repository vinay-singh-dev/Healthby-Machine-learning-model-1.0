# 🧠 AI-Powered Health Tracker

An intelligent skin disease detection system using deep learning (MobileNetV2) and an integrated Dialogflow chatbot to provide personalized health advice and remedies. Built with Python, TensorFlow, and Google Cloud technologies.

---

## 📌 Project Overview

This project uses image recognition to detect 9 common skin diseases and offers chatbot-based health guidance using Dialogflow. It aims to make early detection and basic healthcare more accessible and user-friendly.

---

## ✅ Features

- 📷 **Image-based Skin Disease Classification** using a fine-tuned MobileNetV2 model.
- 🤖 **Dialogflow Chatbot Integration** via Google Cloud for remedies and disease details.
- 📊 **Graphical Visualization** of training progress (loss and accuracy).
- 🧪 **Offline & GUI Support** using Tkinter for user-friendly diagnosis.
- 🔐 **Secure API Credential Handling** (no hardcoded keys).

---

## 🧬 Supported Diseases

| Class Index | Disease Name          |
|-------------|------------------------|
| 0           | Benign Tumors         |
| 1           | Eczema                |
| 2           | Tinea                 |
| 3           | Psoriasis             |
| 4           | Actinic Keratosis     |
| 5           | Vitiligo              |
| 6           | Skin Cancer           |
| 7           | Warts                 |
| 8           | Acne                  |

---

## 🛠️ Tech Stack

- **Frontend:** Tkinter GUI
- **AI/ML:** TensorFlow, Keras, MobileNetV2
- **Visualization:** Matplotlib, Seaborn
- **Chatbot:** Dialogflow ES
- **Cloud:** Google Cloud Console
- **Languages:** Python 3

---

## 🔄 Workflow

```
graph LR
A[User uploads skin image] --> B[MobileNetV2 Model]
B --> C[Predicted Disease]
C --> D[Dialogflow Chatbot]
D --> E[Remedies & Information Shown in GUI]

## 🚀 Demo Instructions

Follow these steps to try the AI-Powered Health Tracker:

### 🔧 Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-health-tracker.git
   cd ai-health-tracker

📦 Install Dependencies
pip install -r requirements.txt

Make sure your requirements.txt includes libraries like:
tensorflow
numpy
pillow
matplotlib
firebase-admin
google-cloud-dialogflow
streamlit

🔐 Add Your Dialogflow Credentials
To enable chatbot functionality:

Go to your Google Cloud Console.

Navigate to your Dialogflow project.

Create a service account key with Dialogflow permissions.

Download the credentials.json file.

Place the file in your project root directory.

Set the environment variable:


