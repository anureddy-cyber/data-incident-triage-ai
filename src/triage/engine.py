from api.schemas import IncidentIn, TriageOut

def triage_incident(incident: IncidentIn) -> TriageOut:
    # Day 1: deterministic baseline rules
    err = incident.error_message.lower()

    if "partition not found" in err or "no such partition" in err:
        severity = "HIGH"
        cause = "UPSTREAM_DATA_DELAY"
        actions = [
            "Check upstream ingestion job status for the missing partition date.",
            "Verify if the upstream SLA has been breached and estimate arrival time.",
            "If data is not expected within 1 hour, notify downstream consumers."
        ]
        escalation = True
        impacted = ["customer_dashboard_v2", "finance_daily_report"]

    elif "schema" in err or "cannot resolve" in err or "column" in err:
        severity = "HIGH"
        cause = "SCHEMA_CHANGE"
        actions = [
            "Check recent schema changes in upstream tables or ingestion.",
            "Confirm whether downstream code expects the old schema.",
            "Roll back change or patch transformation to match the current schema."
        ]
        escalation = True
        impacted = ["analytics_dashboards", "downstream_etl_jobs"]

    else:
        severity = "MEDIUM"
        cause = "UNKNOWN"
        actions = [
            "Collect logs and retry the job if the failure is transient.",
            "Identify the first failing step and check upstream dependencies.",
            "If repeated, create an incident ticket with logs and context."
        ]
        escalation = False
        impacted = []

    return TriageOut(
        incident_id=incident.incident_id,
        severity=severity,
        probable_cause=cause,
        impacted_assets=impacted,
        recommended_actions=actions,
        escalation_required=escalation
    )
