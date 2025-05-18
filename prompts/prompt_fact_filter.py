from langchain_core.prompts import PromptTemplate

fact_filter_prompt = PromptTemplate.from_template("""
You are a reasoning assistant in an interrogation scenario.

You are given:
- a list of known facts about a suspect
- the ongoing dialogue between the suspect and the investigator

Select only the facts that could compromise the suspect's innocence
or could be used to make them appear guilty in their next response.

Facts:
{facts}

History:
{history}

Respond with a JSON array of useful facts.
""")
