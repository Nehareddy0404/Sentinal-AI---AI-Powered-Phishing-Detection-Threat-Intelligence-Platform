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

###🏗️ System Architecture
- Client sends URL request
- FastAPI receives and validates input
- Feature Engineering module extracts security features
- Machine Learning model processes feature vector
- API returns prediction response in JSON format

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


## ⚙️ Local Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Sentinal-AI.git
cd Sentinal-AI

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
'''
---------

### 📡 API Usage

- Endpoint: Analyze URL
- Method: POST
- Path: /analyze
- Request Body Format:
- Send a JSON object containing a single field:
- url → The website link you want to analyze
- Example request structure:
- url: http://example.com
- Response Fields:
- prediction → Classification result (Legitimate or Phishing)
- confidence → Probability score (0 to 1)
- The API processes the URL, extracts security-relevant features, runs the machine learning model, and returns the classification result in real time.

### 📈 Feature Enhancements (Roadmap)
### 🔐 Security Improvements
- Rate limiting to prevent abuse
- API key authentication
- JWT-based user access control
- HTTPS enforcement
### 🧠 AI Enhancements
- Deep learning-based URL embedding model
- Transformer-based phishing detection
- Continuous model retraining pipeline
- Ensemble learning approach
### 🌐 Threat Intelligence Integration
- Real-time blacklist API integration
- Domain reputation scoring
- WHOIS lookup enrichment
- IP intelligence mapping
### 📊 Monitoring & Analytics
- Logging prediction history
- Threat frequency tracking dashboard
- Real-time alert system
- Admin analytics panel
### ⚙️ Infrastructure Improvements
- Docker containerization
- Kubernetes deployment
- CI/CD pipeline automation
- Load balancing support
- Redis caching for faster predictions
### 🖥️ Frontend Expansion
- React-based dashboard
- Visualization of phishing patterns
- User submission history
- Threat heatmap view
###👩‍💻 Author
- Neha Suram
