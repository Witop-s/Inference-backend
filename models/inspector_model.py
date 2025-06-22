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
    event_id: str = Field(..., description="[RW] Unique identifier for this event - use existing IDs to edit known events, don't copy otherwise")
    time: str = Field(..., description="[RW] Timestamp when this event occurred (e.g., '2:30 PM', '2:00-2:30 PM', '2:00 AM J-1')")
    truth: str = Field(..., description="[R] What actually happened at this time (only viewable if discovered)")
    suspect_version: str = Field(default="", description="[RW] The suspect's claimed version of what happened at this time - fill this as you gather information during questioning")
    suspect_supposed_to_know: Union[bool, Literal["unknown"]] = Field(..., description="[RW] Whether the suspect should logically know about this event based on their previous statements or circumstance. true=supposed to know, false=not supposed to know, 'unknown'=unclear if they know")
    inspector_knows: bool = Field(..., description="[X] Whether you are aware of this event - only visible events should be used in questioning")
    suspicion_points_if_revealed: int = Field(..., description="[X] How suspicious it appears if this information surfaces during questioning (higher = more suspicious)")

class TimelineEventInspector(BaseModel):
    event_id: str = Field(..., description="[RW] Unique identifier for this event - use existing IDs to edit known events, don't copy otherwise")
    time: str = Field(..., description="[RW] Timestamp when this event occurred (e.g., '2:30 PM', '2:00-2:30 PM', '2:00 AM J-1')")
    suspect_version: str = Field(default="", description="[RW] The suspect's claimed version of what happened at this time - fill this as you gather information during questioning")
    suspect_supposed_to_know: Union[None, bool, Literal["unknown"]] = Field(..., description="[RW] Whether the suspect should logically know about this event based on their previous statements or circumstance. true=supposed to know, false=not supposed to know, 'unknown'=unclear if they know")

class Evidence(BaseModel):
    evidence_id: str = Field(..., description="[RW] Unique identifier for this evidence - use existing IDs to edit known events, don't copy otherwise")
    description: str = Field(..., description="[R] Description of the physical evidence or testimony")
    suspect_supposed_to_know: Union[bool, Literal["unknown"]] = Field(..., description="[RW] Whether the suspect should logically know about this evidence: true=supposed to know, false=not supposed to know, 'unknown'=unclear if they know")
    inspector_knows: bool = Field(..., description="[X] Whether you are aware of this evidence - only use known evidence in questioning")
    suspicion_points_if_revealed: int = Field(..., description="[X] How much suspicion this evidence generates if brought up (higher = more incriminating)")

class EvidenceInspector(BaseModel):
    evidence_id: str = Field(..., description="[RW] Unique identifier for this evidence - use existing IDs to edit known events, don't copy otherwise")
    suspect_supposed_to_know: Union[None, bool, Literal["unknown"]] = Field(..., description="[RW] Whether the suspect should logically know about this evidence: true=supposed to know, false=not supposed to know, 'unknown'=unclear if they know")

class QuestioningSubject(BaseModel):
    topic: str = Field(..., description="[RW] The subject matter or theme of questions to explore")
    status: str = Field(default="open", description="[RW] Current status of this questioning line: 'open', 'in_progress', 'resolved', 'abandoned'")
    questions_asked: int = Field(default=0, description="[RW] Number of questions asked about this topic so far")
    notes: str = Field(default="", description="[RW] Your notes and observations about the suspect's responses on this topic")

class InspectorPersonality(BaseModel):
    approach: str = Field(..., description="[RW] Your general interrogation approach and demeanor")
    tone: str = Field(..., description="[RW] The emotional tone you should maintain during questioning")
    strategy: str = Field(..., description="[RW] Your overall strategy for conducting this investigation and revealing the truth")

class InspectorWildcard(BaseModel):
    name: str = Field(..., description="[R] Name of the special investigation action (acts as id)")
    description: str = Field(..., description="[R] What this investigation tool does and how it can help uncover evidence")
    uses_left: int = Field(..., description="[RW] Number of times you can still use this tool - use sparingly as they are limited")
    use_tool: bool = Field(default=False, description="[RW] Whether you choose to use this tool on your current reply - set to true to activate it. If true, your speech should be contextual / match your action.")
    how_to_use: str = Field(..., description="[RW] How do you want to use this tool? (e.g. 'Use x on y to try to find out about z') - This use may or may not be successful.")

class SuspectWildcard(BaseModel):
    name: str = Field(..., description="[X] Name of suspect's special investigation action")
    description: str = Field(..., description="[X] What this investigation tool does and how it can help cover evidence")
    uses_left: int = Field(..., description="[X] Number of times the suspect can still use this tool")

class WildcardInspector(BaseModel):
    name: str = Field(..., description="[R] Name of the special investigation action you want to use, copy only if you want to activate it, and fill 'how_to_use' with the action you want to take")
    how_to_use: str = Field(..., description="[RW] How do you want to use this tool? (e.g. 'Use x on y to try to find out about z') - This use may or may not be successful.")
    use_now: bool = Field(default=False, description="[RW] Whether you choose to use this tool on your current reply - set to true to activate it. If true, your speech should be contextual / match your action.")

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
    inspector_personality: InspectorPersonality = Field(..., description="[RW] Your role, approach, and strategy as the investigator")
    inspector_wildcards: List[InspectorWildcard] = Field(..., description="[R] Special investigation tools available to gather additional evidence - use strategically")
    suspect_wildcards: List[SuspectWildcard] = Field(..., description="[X] Special investigation tools available to the suspect")
    end_conditions: EndConditions = Field(..., description="[R] Rules and limits governing how this investigation concludes")

class ScenarioInspector(BaseModel):
    timeline: List[TimelineEventInspector] = Field(..., description="[RW] Chronological sequence of events related to the case - use visible events to build your questioning strategy")
    questioning_subjects: List[QuestioningSubject] = Field(..., description="[RW] Different topics and angles to explore during interrogation.")
    inspector_personality: Union[None, InspectorPersonality] = Field(..., description="[RW] Your role, approach, and strategy as the investigator. You can change it if your current strategy is not working. Else leave blank")
    inspector_wildcards: Union[None, List[WildcardInspector]] = Field(..., description="[RW] Special investigation tools available to gather additional evidence - use strategically. Leave blank if not using")

class DialogueMessage(BaseModel):
    role: Literal["investigator", "suspect"] = Field(..., description="[R] Role of the speaker in the dialogue")
    content: str = Field(..., description="[R] The actual message content spoken by the role")

class JsonInput(BaseModel):
    dialogue: List[DialogueMessage] = Field(..., description="[R] The ongoing dialogue between the investigator and the suspect")
    scenario: Scenario = Field(..., description="[R] The current scenario of the investigation, including context, charges, timeline, etc. This is used to keep track of the investigation and the suspect's responses. You are free to edit fields marked as [RW] (read-write) in the scenario model, but you should not edit fields marked as [R] (read-only).")