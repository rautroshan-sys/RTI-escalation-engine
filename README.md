# ⚖️ RTI Escalation Engine

**A Smart India Hackathon Prototype**

An AI-powered triage and routing system designed to automate the classification of Right to Information (RTI) applications. This system uses semantic vector mapping to instantly route queries to the correct government department and automatically flags ambiguous or complex requests for manual review, ensuring strict compliance with Section 6(3) of the RTI Act.

## ✨ Key Features

* **Zero-Shot Semantic Routing:** Replaces rigid keyword matching with `sentence-transformers`, mapping user queries to department vectors in multidimensional space for highly accurate classification without requiring hardcoded training data.
* **Automated Section 6(3) Escalation:** Intelligently detects low-confidence queries and halts automated routing, generating a recommended statutory appeal pathway for manual review.
* **Privacy-First Audit Logging:** Uses SHA-256 hashing to log transaction records in a local SQLite database without exposing Personally Identifiable Information (PII) from the raw queries.
* **Dynamic React Dashboard:** A responsive, Vite-powered UI that visualizes AI confidence scores and routing decisions in real-time.

## 🛠️ Tech Stack

* **Frontend:** React, Vite, Tailwind CSS
* **Backend:** FastAPI, Python, SQLAlchemy, SQLite
* **AI/ML Engine:** PyTorch, Hugging Face Transformers (`all-MiniLM-L6-v2`)

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/RTI-escalation-engine.git](https://github.com/yourusername/RTI-escalation-engine.git)
cd RTI-escalation-engine
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
cd frontend
npm install
cd ..
```

### 3. Run the Backend
```bash
uvicorn app.main:app --reload
```

### 4. Run the Frontend
```bash
cd frontend
npm run dev
```

The backend starts on `http://127.0.0.1:8000` and the frontend runs on Vite's default development server.