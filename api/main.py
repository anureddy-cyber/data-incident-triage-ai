from fastapi import FastAPI
from api.schemas import IncidentIn, TriageOut
from src.triage.engine import triage_incident

app = FastAPI(title="Data Incident Triage Service", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/triage", response_model=TriageOut)
def triage(payload: IncidentIn):
    return triage_incident(payload)
