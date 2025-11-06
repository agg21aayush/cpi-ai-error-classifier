from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ErrorRequest(BaseModel):
    errorText: str

@app.post("/classifyError")
def classify_error(req: ErrorRequest):
    t = req.errorText.lower()
    if "401" in t or "unauthorized" in t:
        return {"errorCategory": "Authentication", "confidence": 0.95,
                "recommendedAction": "Renew access token or check credentials"}
    if "timeout" in t:
        return {"errorCategory": "Network", "confidence": 0.9,
                "recommendedAction": "Retry after short delay"}
    if "mapping" in t or "cannot convert" in t:
        return {"errorCategory": "Mapping", "confidence": 0.88,
                "recommendedAction": "Check message mapping structure"}
    if "idoc" in t:
        return {"errorCategory": "SAP IDoc", "confidence": 0.85,
                "recommendedAction": "Verify IDoc segment structure"}
    return {"errorCategory": "Unknown", "confidence": 0.6,
            "recommendedAction": "Manual investigation required"}
