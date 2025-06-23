from pydantic import BaseModel, Field
from typing import List

from models.inspector_model import DialogueMessage, Scenario, TimelineEvent, Evidence, InspectorWildcard

class ScenarioGamemaster(BaseModel):
    timeline: List[TimelineEvent] = Field(..., description="[RW] Chronological sequence of events related to the case")
    evidence: List[Evidence] = Field(..., description="[R] Physical evidence and testimony available")
    inspector_wildcards: List[InspectorWildcard] = Field(..., description="[R] Special investigation tools available to gather additional evidence")

class JsonOutput(BaseModel):
    dialogue: List[DialogueMessage]
    scenario: ScenarioGamemaster
    suspicion_points: int = Field(..., ge=0, description="Total suspicion points accumulated by the inspector, used to assess the suspect's credibility")