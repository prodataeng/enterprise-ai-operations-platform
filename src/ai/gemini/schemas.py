from pydantic import BaseModel

class BusinessAnalysis(BaseModel):
    summary: str
    finding: str
    recommended_action: str
    confidence: str