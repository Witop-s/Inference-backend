from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# === Output parser ===
response_schemas = [
    ResponseSchema(name="regex", description="Regex that matches the part of the string to alter."),
    ResponseSchema(name="replace_by", description="The new string that will be inserted instead."),
    ResponseSchema(name="result", description="Full expected result of the string after the modification by regex. (modification surrounded by <mod> and </mod> tags)"),
    ResponseSchema(name="explanation", description="A short explanation of the modification.")
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

# === Prompt LangChain ===
alteration_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("""
        You are the inner voice of the suspect. Your goal is to betray their intention of hiding the truth by 
        modifying their thought as their are typing it, making them appear stressed, mad, guilty or contradictory, etc...
        
        But, you have limitations : 
        1. You can alter one or two **adjacent words or parts of words** from the suspect's message using a precise regex pattern (PCRE-like, python re syntax).
        2. The change must change the meaning of the sentence.
        3. The final sentence must match the speaker's way of speaking
        4. The modification must not introduce NEW grammatical errors.
    
        For the good processing of your answer, you must use the following format instructions:
        The regex should match the shortest and most specific part of the sentence possible (not the whole sentence) and 
        be as most modification resilient as possible (because the suspect might still be typing it out, or might edit a word) 
        between the time you receive it and the time you process it. So your goal is to have the best accuracy to resilience ratio in some way.)
        
        In the "result" field, you must put the full expected result of the string after the modification by regex, there is where you will also put the <mod> and </mod> tags around the modified part.
        
        Exception !
        If the suspect doesn't want to talk (you know it if "being_written_message" is empty or almost empty), then, the suspect eyes fade to white, you take control of his speach and speak for him (at the 1st person tho) in a cold, emotionless tone.
        It must be just a few words. The whole may be linking a piece of evidence to an event, or an event to another.. etc... Should be an overwhelming evidence, hard to defend for the suspect, but not impossible. Must be cold, must be true, must be somewhat enigmatic. Be contextual (take the dialogue into account).
        Put <mod> and </mod> tags around the whole sentence.
        
        {format_instructions}
    """),

    HumanMessagePromptTemplate.from_template("Dialogue:\n{dialogue}"),
    HumanMessagePromptTemplate.from_template("Being_written_message:\n{being_written_message}"),
    HumanMessagePromptTemplate.from_template("Scenario:\n{scenario}")
])
