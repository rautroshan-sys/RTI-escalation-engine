# Hackathon Execution Constraints & Directives

## 1. Project Goal
Build a multilingual Right to Information (RTI) document classifier that predicts the top 2 government departments with calibrated confidence. The core value proposition is **Safe Escalation**: the system must explicitly refuse to auto-route ambiguous cases or cases with known jurisdictional overlap, thereby automating compliance with Section 6(3) of the RTI Act.

## 2. Hard Constraints for AI Agents
- **Time Limit:** We are operating in a 10-hour sprint. Do not over-engineer.
- **Tech Stack (STRICT):** 
  - Backend: Python, FastAPI, Pydantic.
  - Database: SQLite (with Alembic for migrations). 
  - AI Model: IndicBERT (via HuggingFace) running locally.
  - Frontend: React (Single Page Application).
- **Prohibited Tech:** DO NOT use Redis, Celery, Docker, Kafka, or GraphQL unless explicitly instructed by a human developer.
- **Security:** Do not store raw RTI text in the database to ensure privacy compliance. Store only the SHA-256 hash of the input text.

## 3. The 4 Demo Test Cases
Ensure the system natively handles these 4 flows:
1. **Clear (Hindi):** Road repair -> Auto-route to PWD.
2. **Clear (Marathi):** Ration card -> Auto-route to RATION.
3. **Low Confidence (English):** "Water pipeline in society" -> Scores for WATER and PWD are close -> ESCALATE.
4. **State Overlap (Hindi):** "Street lights & municipal roads" -> Triggers explicit overlap rule -> ESCALATE.