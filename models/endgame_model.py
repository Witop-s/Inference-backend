from pydantic import BaseModel, Field

class JsonOutput(BaseModel):
    inspector_closing_sentence: str = Field(..., description="The closing sentence of the inspector at the end of the interrogation, written in a film script style.")
    recap: str = Field(..., description="A quick recap of the interrogation, including the main points and the outcome, written in a film script style.")
    suspect_score: int = Field(..., ge=0, le=100, description="A number from 0 to 100 representing the inspector's assessment of the suspect's guilt, where 0 = innocent and 100 = guilty.")
