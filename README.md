🏥 MediCare+ Health Platform
AI-powered healthcare web application for symptom analysis and personalized health recommendations.
✨ Features

🤖 AI Symptom Analysis - Get instant health advice based on your symptoms

📄 PDF Reports - Download professional health reports
📱 Responsive Design - Works on all devices


🚀 Quick Start

clone the    repo

Configure Firebase

Update Firebase config in index.html with your credentials


Set up Backend API

Configure /predict endpoint for symptom analysis


Run

bash   python -m http.server 8000
Open http://localhost:127.0.0.1:5000
🛠️ Tech Stack

HTML5, CSS3, JavaScript
Firebase Firestore
jsPDF (PDF generation)


📋 API Format
POST /predict
json{
  "symptoms": "fever, headache",
  "last_meal": "curry",
  "duration": "2"
}
⚠️ Disclaimer
This is for educational purposes only. Not a substitute for professional medical advice.
📄 License
MIT License

⭐ Star this repo if you find it helpful!
