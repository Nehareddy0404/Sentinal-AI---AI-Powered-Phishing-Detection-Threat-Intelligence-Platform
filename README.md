# 🛡️ Sentinal AI  
## AI-Powered Phishing Detection & Threat Intelligence Platform

🔗 **Live API:**  
https://sentinal-ai-ai-powered-phishing.onrender.com  

Sentinal AI is a cloud-deployed machine learning system that detects phishing URLs using advanced feature engineering, domain intelligence analysis, and real-time API inference.

Built to simulate modern cybersecurity threat detection infrastructure.

---

## 🚀 Overview

Phishing attacks remain one of the most common and dangerous cyber threats.  
Sentinal AI analyzes URLs in real time and predicts whether they are:

- ✅ Legitimate  
- 🚨 Malicious (Phishing)

The system extracts structural, domain-level, and behavioral URL features before applying machine learning classification.

This backend is fully deployed in production using **FastAPI** and **Render**.

---

## 🧠 Key Features

### 🔍 Advanced URL Feature Engineering
- Domain length analysis
- Subdomain extraction & depth calculation
- Suspicious character detection
- URL length & structural complexity
- Entropy-based randomness scoring
- Keyword-based phishing detection

### 🌐 Domain Intelligence
- TLD parsing using `tldextract`
- Suspicious TLD identification
- Subdomain pattern inspection
- URL anomaly detection

### ⚡ Real-Time API Inference
- FastAPI-based REST endpoints
- JSON request/response handling
- Low-latency predictions
- Automatic Swagger documentation (`/docs`)

### ☁️ Production Deployment
- Hosted on Render
- GitHub-based CI/CD
- Production-grade Uvicorn server
- Environment-based configuration

---

## 🏗️ System Architecture

Client Request
↓
FastAPI Endpoint
↓
Feature Engineering Module
↓
Machine Learning Model
↓
Prediction Response (JSON)

----

### Core Components

- `backend/main.py` → FastAPI application & API routes  
- `feature_engine.py` → Feature extraction engine  
- ML Model → URL classification logic  
- Render → Cloud deployment platform  

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- Uvicorn
- Pydantic
- Python 3.11+

### Feature Engineering & Security
- tldextract
- Custom regex-based URL parsing
- Entropy calculations
- Structural anomaly detection

### Networking
- requests
- httpx

### Environment Management
- python-dotenv

### Deployment
- Render Web Service
- GitHub CI/CD Integration

---

## 📂 Project Structure

Sentinal-AI/
│
├── backend/
│ ├── main.py
│
├── feature_engine.py
├── requirements.txt
├── README.md

-----

---

## ⚙️ Local Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Sentinal-AI.git
cd Sentinal-AI
'''

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Development Server
uvicorn backend.main:app --reload

Server runs at:
http://127.0.0.1:8000

📡 API Usage
Endpoint: Analyze URL
Request Body Example
{
  "url": "http://example.com"
}
Response Example
{
  "prediction": "Legitimate",
  "confidence": 0.93
}
🧪 How It Works
Client sends URL to FastAPI endpoint
Feature engine extracts security-relevant features
ML model processes feature vector
API returns classification result

🌍 Production Details
Deployed on Render (Free Tier)
Auto redeploy on GitHub push
Dependency-managed environment
Production Uvicorn server configuration

Live Endpoint:
https://sentinal-ai-ai-powered-phishing.onrender.com

📈 Future Enhancements
Frontend Dashboard (React / Next.js)
Database integration for threat logging
Blacklist API integration
Real-time domain reputation lookup
Model retraining pipeline
Docker containerization
Rate limiting & authentication
Threat intelligence analytics dashboard

👩‍💻 Author
Neha Suram
