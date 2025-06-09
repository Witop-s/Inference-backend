from pydantic import BaseModel, Field
from typing import List, Union, Literal

class Context(BaseModel):
    title: str = Field(..., description="[R] Title of the investigation case")
    description: str = Field(..., description="[R] Background context and setting for the investigation")
    setting: str = Field(..., description="[R] Physical location where the interrogation takes place")
    inspector: str = Field(..., description="[R] Your role/identity as the investigator")
    suspect_name: str = Field(..., description="[R] Name of the person you are questioning")
    suspect_age: int = Field(..., description="[R] Age of the suspect being questioned")

class Charges(BaseModel):
    primary_charge: str = Field(..., description="[R] The main accusation or crime being investigated")

class TimelineEvent(BaseModel):
    time: str = Field(..., description="[RW] Timestamp when this event occurred (e.g., '2:30 PM', '2:00-2:30 PM', '2:00 AM J-1')")
    truth: str = Field(..., description="[X] What actually happened at this time")
    suspect_version: str = Field(default="", description="[RW] The suspect's claimed version of what happened at this time - fill this as you gather information during questioning")
    suspect_supposed_to_know: bool = Field(..., description="[RW] Whether the suspect should logically know about this event based on their previous statements or circumstances")
    inspector_knows: bool = Field(..., description="[X] Whether you are aware of this event - only visible events should be used in questioning")
    suspicion_points_if_revealed: int = Field(..., description="[X] How suspicious it appears if this information surfaces during questioning (higher = more suspicious)")

class Evidence(BaseModel):
    description: str = Field(..., description="[X] Description of the physical evidence or testimony")
    suspect_supposed_to_know: Union[bool, Literal["unknown"]] = Field(..., description="[RW] Whether the suspect should logically know about this evidence: true=supposed to know, false=not supposed to know, 'unknown'=unclear if they know")
    inspector_knows: bool = Field(..., description="[X] Whether you are aware of this evidence - only use known evidence in questioning")
    suspicion_points_if_revealed: int = Field(..., description="[X] How much suspicion this evidence generates if brought up (higher = more incriminating)")

class QuestioningSubject(BaseModel):
    topic: str = Field(..., description="[RW] The subject matter or theme of questions to explore")
    status: str = Field(default="open", description="[RW] Current status of this questioning line: 'open', 'in_progress', 'resolved', 'abandoned'")
    questions_asked: int = Field(default=0, description="[RW] Number of questions asked about this topic so far")
    notes: str = Field(default="", description="[RW] Your notes and observations about the suspect's responses on this topic")

class InspectorPersonality(BaseModel):
    approach: str = Field(..., description="[RW] Your general interrogation approach and demeanor")
    tone: str = Field(..., description="[RW] The emotional tone you should maintain during questioning")
    strategy: str = Field(..., description="[RW] Your overall strategy for conducting this investigation and revealing the truth")

class Wildcard(BaseModel):
    name: str = Field(..., description="[R] Name of the special investigation action")
    description: str = Field(..., description="[R] What this investigation tool does and how it can help uncover evidence")
    uses_left: int = Field(..., description="[RW] Number of times you can still use this tool - use sparingly as they are limited")
    use_tool: bool = Field(default=False, description="[RW] Whether you choose to use this tool on your current reply - set to true to activate it. If true, your speech should be contextual / match your action.")
    how_to_use: str = Field(..., description="[RW] How do you want to use this tool? (e.g. 'Use x on y to try to find out about z') - This use may or may not be successful.")

class EndConditions(BaseModel):
    suspicion_threshold: int = Field(..., description="[X] Suspicion level needed to consider the case solved (you're building toward this)")
    max_questions: int = Field(..., description="[R] Maximum number of questions you can ask before the investigation ends (RP: time limit)")
#    max_wildcards_used: int = Field(..., description="Maximum number of wildcard tools that can be used in total")
#    confession_ends_game: bool = Field(..., description="Whether a full confession from the suspect immediately ends the investigation")
    current_questions: int = Field(default=0, description="[R] Number of questions asked so far - automatically tracked")

class Scenario(BaseModel):
    id: str = Field(..., description="[X] Unique identifier for this investigation scenario")
    difficulty: str = Field(..., description="[X] Difficulty level of this case (beginner, intermediate, advanced)")
    max_suspicion: int = Field(..., description="[X] Maximum suspicion points possible in this case")
    context: Context = Field(..., description="[R] Background information and setting for your investigation")
    charges: Charges = Field(..., description="[R] The accusations you are investigating")
    timeline: List[TimelineEvent] = Field(..., description="[RW] Chronological sequence of events related to the case - use visible events to build your questioning strategy")
    evidence: List[Evidence] = Field(..., description="[R] Physical evidence and testimony available - only use evidence you know about")
    questioning_subjects: List[QuestioningSubject] = Field(..., description="[RW] Different topics and angles to explore during interrogation")
    inspector_personality: InspectorPersonality = Field(..., description="[R] Your role, approach, and strategy as the investigator")
#    wildcards: List[Wildcard] = Field(..., description="[R] Special investigation tools available to gather additional evidence - use strategically")
    end_conditions: EndConditions = Field(..., description="[R] Rules and limits governing how this investigation concludes")