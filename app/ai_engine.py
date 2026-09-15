import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

class RTIRouter:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("l3cube-pune/indic-sentence-similarity-sbert")
        self.model = AutoModelForSequenceClassification.from_pretrained("l3cube-pune/indic-sentence-similarity-sbert", num_labels=10)
        self.departments = ["PWD", "WATER", "EDU", "HEALTH", "RATION", "POLICE", "TRANSPORT", "ELEC", "MUNI", "REV"]
        self.overlap_sets = [{"MUNI", "PWD"}, {"WATER", "MUNI"}]

    def predict(self, text: str, state_code: str = None) -> dict:
        with torch.no_grad():
            probs = F.softmax(self.model(**self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)).logits, dim=1)[0].tolist()
        
        dept_scores = sorted(zip(self.departments, probs), key=lambda x: x[1], reverse=True)[:2]
        
        if dept_scores[0][1] < 0.85:
            return self._build_response(dept_scores, "ESCALATE", f"Low confidence: {dept_scores[0][1]*100:.1f}%")
        if (dept_scores[0][1] - dept_scores[1][1]) < 0.15:
            return self._build_response(dept_scores, "ESCALATE", f"Narrow margin between {dept_scores[0][0]} and {dept_scores[1][0]}")
        if any(o.issubset({dept_scores[0][0], dept_scores[1][0]}) for o in self.overlap_sets):
            return self._build_response(dept_scores, "ESCALATE", f"Jurisdictional overlap in {state_code or 'general'}: {dept_scores[0][0]} & {dept_scores[1][0]}")
        
        return self._build_response(dept_scores, "AUTO_ROUTE", None)

    def _build_response(self, scores, decision, reason):
        return {
            "predictions": [{"department_id": s[0], "confidence_score": round(s[1], 4)} for s in scores],
            "decision": decision,
            "escalation_reason": reason
        }

rti_engine = RTIRouter()