from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(
    title="Smart-SOC API",
    description="ML-Based Threat Triage with Explainable AI",
    version="1.0.0",
)


class TrafficSample(BaseModel):
    src_ip: str
    dst_ip: str
    protocol: str
    bytes_sent: int
    packets: int
    duration: float
    flags: Optional[str] = None


class TriageResult(BaseModel):
    label: str
    confidence: float
    severity: str
    explanation: str
    recommended_action: str


@app.get("/")
def root():
    return {
        "service": "Smart-SOC Threat Triage",
        "status": "operational",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/triage", response_model=TriageResult)
def triage_traffic(sample: TrafficSample):
    """
    Analyze a network traffic sample and return ML-driven triage result.
    Placeholder logic — replace with real XGBoost + SHAP inference.
    """
    # Placeholder scoring logic (swap with real model inference)
    score = (sample.bytes_sent / 1000) + (sample.packets * 0.1)

    if score > 50:
        return TriageResult(
            label="DDoS",
            confidence=0.91,
            severity="CRITICAL",
            explanation="High packet volume with large byte transfer. "
            "Top features: bytes_sent, packets.",
            recommended_action="Block source IP immediately and escalate to L2.",
        )
    elif score > 20:
        return TriageResult(
            label="Port Scan",
            confidence=0.78,
            severity="MEDIUM",
            explanation="Short duration, multiple packets with low byte count. "
            "Reconnaissance pattern.",
            recommended_action="Monitor source IP and add to watchlist.",
        )
    else:
        return TriageResult(
            label="Benign",
            confidence=0.85,
            severity="LOW",
            explanation="Traffic pattern within normal thresholds.",
            recommended_action="No action required.",
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)  # nosec B104
