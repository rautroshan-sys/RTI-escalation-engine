# System Architecture & Flow

## 1. Component Pipeline
1. **Frontend (React):** User submits RTI text.
2. **API Layer (FastAPI):** Receives POST request, validates payload via Pydantic.
3. **Inference Layer:** Passes text to IndicBERT (loaded in memory). Returns top 2 departments and probability scores.
4. **Rules Engine:** Applies threshold logic and overlap rules defined in `02_legal_domain_context.md`. Determines if `final_decision` is "AUTO_ROUTE" or "ESCALATE".
5. **Appeal Generator:** If "ESCALATE", attaches a draft First Appeal letter payload citing Section 6(3).
6. **Audit Logger:** Hashes the input text using SHA-256 and writes the transaction to SQLite.

## 2. Database Schema (SQLite)
Table: `audit_logs`
- `id`: UUID (Primary Key)
- `timestamp`: DateTime
- `input_hash`: String (SHA-256)
- `predicted_dept_1`: String
- `score_1`: Float
- `predicted_dept_2`: String
- `score_2`: Float
- `final_decision`: String ("AUTO_ROUTE" | "ESCALATE")
- `human_override`: String (Nullable)

## 3. Visual Execution Pipeline

[Frontend (React)]
        |
        | HTTP POST /classify (JSON payload)
        v
[FastAPI Backend]
        |
        | 1) Validate request schema (Pydantic)
        | 2) Call AI service inference function
        | 3) Apply routing & overlap rules
        | 4) Fetch appeal pathway (RAG-lite / JSON Config)
        | 5) Log transaction to DB (SQLite hash audit)
        | 6) Return structured Pydantic response
        v
[AI/ML Service (IndicBERT)]
        |
        | - Load multilingual encoder weights
        | - Predict probabilities across 10 classes
        | - Return Top 2 departments + scores
        v
[Data & Config Layer]
        - Department taxonomy config
        - Overlap rules (subject+state -> multiple depts)
        - Appeal rules (dept+state -> authority, timeline)
        - Threshold config (Escalate if gap < 0.15)