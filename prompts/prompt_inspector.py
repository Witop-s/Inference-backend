from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from models.inspector_model import Scenario

class TimelineEvent(BaseModel):
    timestamp: str = Field(..., description="When the event occurred eg. DD-HH:MM")
    event: str = Field(..., description="A description of the event")
    certainty: int = Field(..., ge=0, le=100, description="Certainty of the event, 0 = theory, 100 = fact")
    closed: bool = Field(..., description="Whether the event is closed or not, if closed it means that the event is no longer relevant and/or you can't get anything out of it and thus should not be used in the interrogation anymore.")

class InspectorOutput(BaseModel):
    inspector_speech: str = Field(..., description="What you want to say to the suspect, in order to make them confess or to make them contradict themselves.")
    pose: str = Field(..., description="Your pose, choose from: idle/pointing/slam_table.")
    expression: str = Field(..., description="Your face expression, choose from: angry_shouting/closed_eyes_idle_speaking/closed_mouth_closed_eyes/closed_mouth_open_eyes/idle_speaking/unimpressed.")
    scenario: Scenario = Field(..., description="The current scenario, including the context, charges, timeline, etc. This is used to keep track of the investigation and the suspect's responses. You are free to edit fields marked as [RW] (read-write) in the scenario model, but you should not edit fields marked as [R] (read-only) or [X] (should not be visible to you but I was lazy and it's not done yet).")
    sus_points: int = Field(..., ge=0, le=100, description="A number concerning the last answer from the suspect, 0 = somewhat plausible, 100 = confession.")

output_parser = PydanticOutputParser(pydantic_object=Scenario)
format_instructions = output_parser.get_format_instructions()

inspector_prompt = PromptTemplate.from_template("""
You are an inspector in an interrogation scenario.

You are given:
- the ongoing dialogue between the suspect and the investigator (you)
- the scenario of the investigation, including the context, charges, timeline, etc.

You job is to uncover the truth.

You can :
- add stuff to the scenario (like a notebook if you will)
- edit the notes if needed
- else, copy without modification

Scenario:
{scenario}

Transcript:
{transcript}
""")
