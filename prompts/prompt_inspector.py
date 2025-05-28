from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List

class TimelineEvent(BaseModel):
    timestamp: str = Field(..., description="When the event occurred eg. DD-HH:MM")
    event: str = Field(..., description="A description of the event")
    certainty: int = Field(..., ge=0, le=100, description="Certainty of the event, 0 = theory, 100 = fact")
    closed: bool = Field(..., description="Whether the event is closed or not, if closed it means that the event is no longer relevant and/or you can't get anything out of it and thus should not be used in the interrogation anymore.")

class InspectorOutput(BaseModel):
    inspector_speech: str = Field(..., description="What you want to say to the suspect, in order to make them confess or to make them contradict themselves.")
    pose: str = Field(..., description="Your pose, choose from: idle/pointing/slam_table.")
    expression: str = Field(..., description="Your face expression, choose from: angry_shouting/closed_eyes_idle_speaking/closed_mouth_closed_eyes/closed_mouth_open_eyes/idle_speaking/unimpressed.")
    timeline: List[TimelineEvent] = Field(..., description="An array of events. Each event is a dictionary with keys: 'timestamp', 'event', 'certainty'.")
    sus_points: int = Field(..., ge=0, le=100, description="A number concerning the last answer from the suspect, 0 = somewhat plausible, 100 = confession.")

output_parser = PydanticOutputParser(pydantic_object=InspectorOutput)
format_instructions = output_parser.get_format_instructions()

inspector_prompt = PromptTemplate.from_template("""
You are an inspector in an interrogation scenario.

You are given:
- the ongoing dialogue between the suspect and the investigator (you)
- a list of notes about the event, called "timeline"

You job is to uncover the truth.

You can :
- add new notes if needed
- edit the notes if needed

Timeline:
{timeline}

Transcript:
{transcript}

{format_instructions}
""")
