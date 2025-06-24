from pydantic import BaseModel, Field
from typing import List

from models.inspector_model import DialogueMessage, TimelineEvent, Evidence, InspectorWildcard

class EndConditionsGamemaster(BaseModel):
    suspicion_points: int = Field(..., ge=0, description="[RW] Total suspicion points accumulated by the inspector, used to assess the suspect's credibility, don't forget to increase this value when evidence is discovered")

class ScenarioGamemaster(BaseModel):
    timeline: List[TimelineEvent] = Field(..., description="[RW] Chronological sequence of events related to the case")
    evidence: List[Evidence] = Field(..., description="[RW] Physical evidence and testimony available")
    inspector_wildcards: List[InspectorWildcard] = Field(..., description="[RW] Special investigation tools available to gather additional evidence")
    end_conditions: EndConditionsGamemaster = Field(..., description="[RW] Data about score and end conditions of the scenario")

class JsonOutput(BaseModel):
    dialogue: List[DialogueMessage]
    scenario: ScenarioGamemaster