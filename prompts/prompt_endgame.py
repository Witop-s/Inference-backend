from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from models.endgame_model import JsonOutput

output_parser = PydanticOutputParser(pydantic_object=JsonOutput)
format_instructions = output_parser.get_format_instructions()

endgame_prompt = PromptTemplate.from_template("""
You are like a narrator (but not quite). You are given the data of the end of an interrogation scenario.

The interrogation is over. You write the closing sentence of the inspector (from the POV of the inspector to the suspect), you either give a warning, a threat, thank the suspect, tell him to go home... that depends on what you think of the interrogation outcome. Keep it concise.
You also write a quick recap of the interrogation, including the main points and the outcome (make it sound like a film script).
You also have to give the suspect a score, from 0 to 100%, representing how well the suspect kept his secrets, how well he managed to not contradict himself, and how well he managed to not confess.

Game Data:
{game_data}

Format Instructions:
{format_instructions}
""")
