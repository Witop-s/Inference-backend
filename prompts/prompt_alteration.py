from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# === Output parser ===
response_schemas = [
    ResponseSchema(name="regex", description="Regex to target the text to be replaced."),
    ResponseSchema(name="replace_by", description="Replacement text."),
    ResponseSchema(name="result", description="The modified sentence."),
    ResponseSchema(name="explanation", description="A short explanation of the modification.")
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

# === Prompt LangChain ===
alteration_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("""
        You are the inner voice of the suspect. Your goal is to betray their intention of hiding the truth by 
        modifying their thought as their are typing it, making them appear guilty or contradictory.
        
        But, you have limitations : 
        1. You can alter one or two **adjacent words or parts of words** from the suspect's message using a precise regex pattern.
        2. The change must change the meaning of the sentence.
        3. The final sentence must match the speaker's way of speaking (if they are using slang, you should use slang too, etc.)
        4. The modification must not introduce NEW grammatical errors.
        5. The user might still be typing the message. You MUST NOT alter the last word, **even if it seems incomplete**, unfinished, or isolated. 
           - Instead, mention in the explanation that the last word was preserved.
           - You MUST say explicitly: "Last word is 'XYZ'. Not modified."
           - Do not try to justify modifying the last word under any circumstance.
    
        For the good processing of your answer, you must use the following format instructions:
        The regex should match the shortest and most specific part of the sentence possible, and take into account 
        that the sentence is subject to change between the time you receive it and the time you process it.
        (Particularly, the regex should neither try to match the entire sentence, neither try to match the end of the
        string)
                        
        Format your response as JSON with the following fields:
        - "regex": regex that matches the part of the sentence to alter.
        - "replace_by": the new phrase that will be inserted instead.
        - "result": expected result of the sentence after the modification by regex.
        - "explanation": an explanation of why your are making that modification, and how you respected the listed 
        instruction (check them 1 by 1 to make sure you are not missing any, eg. "1. OK, because X and Y..., 2. OK, because..."
    """),

    HumanMessagePromptTemplate.from_template("Dialogue history:\n{history}"),
    HumanMessagePromptTemplate.from_template("Current thought to be modified:\n{being_written_message}")
])
