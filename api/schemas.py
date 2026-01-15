from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Severity = Literal["LOW", "MEDIUM", "HIGH"]

class IncidentIn(BaseModel):
    incident_id: str = Field(..., examples=["INC-1001"])
    source: str = Field(..., examples=["airflow"])
    job_name: Optional[str] = Field(None, examples=["daily_customer_metrics"])
    table: Optional[str] = Field(None, examples=["analytics.customer_metrics_daily"])
    error_message: str = Field(..., examples=["Partition not found for date 2026-01-14"])
    event_time: str = Field(..., examples=["2026-01-15T02:10:00Z"])

class TriageOut(BaseModel):
    incident_id: str
    severity: Severity
    probable_cause: str
    impacted_assets: List[str]
    recommended_actions: List[str]
    escalation_required: bool
