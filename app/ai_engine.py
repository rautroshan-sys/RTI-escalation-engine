import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

class RTIRouter:
    def __init__(self):
        # We use a fast, pre-trained sentence transformer for Semantic Vector Mapping
        # This requires zero fine-tuning!
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

        # We define the departments and their semantic "threat/issue" words
        self.departments = {
            "PWD": "Public works, road maintenance, potholes, construction, highways, bridges.",
            "WATER": "Water supply, broken pipes, drainage, sewage, drinking water shortage.",
            "ELEC": "Electricity, power cuts, broken streetlights, transformers, wiring.",
            "POLICE": "Law enforcement, crime, FIR, theft, violence, security, murder.",
            "MUNI": "Municipal corporation, garbage collection, property tax, sanitation.",
            "HEALTH": "Public health, hospitals, clinics, disease outbreak, medical negligence.",
            "EDU": "Education, government schools, teachers, syllabus, exams, university.",
            "RATION": "Public distribution, ration cards, food supply, subsidies, grain.",
            "TRANSPORT": "Public transport, buses, train schedules, RTO, driving license.",
            "REV": "Revenue department, land records, certificates, stamp duty, property registration."
        }
        self.dept_keys = list(self.departments.keys())

        # Pre-compute the vectors (embeddings) for all 10 departments on startup
        self.dept_embeddings = self._get_embeddings(list(self.departments.values()))

    def _get_embeddings(self, texts):
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=128)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Mean pooling to get a single vector per sentence
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return F.normalize(embeddings, p=2, dim=1)

    def predict(self, text: str, state_code: str = None) -> dict:
        # 1. Convert the user's RTI query into a vector
        query_embedding = self._get_embeddings([text])

        # 2. Calculate cosine similarity between the query and all department vectors
        similarities = torch.mm(query_embedding, self.dept_embeddings.transpose(0, 1))[0]

        # 3. Grab the top 2 highest scoring departments
        top_scores, top_indices = torch.topk(similarities, 2)
        top_scores = top_scores.tolist()
        top_indices = top_indices.tolist()

        dept_scores = [(self.dept_keys[idx], score) for idx, score in zip(top_indices, top_scores)]

        # 4. Routing Logic (Cosine similarity scores are lower than standard softmax probabilities, so we adjust the threshold)
        confidence = dept_scores[0][1]
        if confidence < 0.35:
            return self._build_response(dept_scores, "ESCALATE", f"Low semantic confidence: {confidence*100:.1f}%. Requires manual review per Section 6(3).")

        return self._build_response(dept_scores, "AUTO_ROUTE", None)

    def _build_response(self, scores, decision, reason):
        return {
            "predictions": [{"department_id": s[0], "confidence_score": round(s[1], 4)} for s in scores],
            "decision": decision,
            "escalation_reason": reason
        }

# Initialize a single instance to be used by the API
rti_engine = RTIRouter()