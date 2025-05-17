import logging
import azure.functions as func
from dotenv import load_dotenv
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# Initialize the Mistral AI model
llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.7,
    max_retries=2
)

llm_filter = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.2,
    max_retries=2
)

fact_filter_prompt = PromptTemplate.from_template("""
You are a reasoning assistant in an interrogation scenario.

You are given:
- a list of known facts about a suspect
- the ongoing dialogue between the suspect and the investigator

Select only the facts that could compromise the suspect's innocence or that could be used to make them appear guilty in his next response.

Facts:
{facts}

History:
{history}

Respond with a JSON array of useful facts.
""")

select_facts_chain = (
        RunnableMap({
            "facts": lambda x: x["facts"],
            "history": lambda x: "\n".join([f'{m["role"]}: {m["content"]}' for m in x["history"]])        })
        | fact_filter_prompt
        | llm_filter
)

# Define the schema
response_schemas = [
    # ResponseSchema(name="action", description="Action to take, either 'replace', 'delete', 'add', or 'swap'. (Only descriptive, does not affect the message)"),
    ResponseSchema(name="regex", description="Regex to target the text to be replaced. (Be as precise as possible)"),
    ResponseSchema(name="replace_by", description="Replacement text."),
    ResponseSchema(name="result", description="The modified sentence after applying the regex and replacement.")
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

app = func.FunctionApp()

@app.route(route="inner-voice-fact-filter", auth_level=func.AuthLevel.ANONYMOUS)
def inner_voice_fact_filter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger : inner-voice-fact-filter')

    try:
        body_json = req.get_json()

        # Invoke the Mistral AI model
        ai_response = select_facts_chain.invoke(body_json)

        return func.HttpResponse(
            ai_response.content,
            status_code=200,
            mimetype="text/plain"
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(
            "An error occurred.",
            status_code=500
        )

@app.route(route="inner-voice", auth_level=func.AuthLevel.ANONYMOUS)
def inner_voice(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger inner-voice')

    try:
        body_json = req.get_json()
        being_written_message = body_json['being_written_message']
        history = body_json['history']

        print(being_written_message)
        print(history)

        # Prepare the message sequence
        messages = [
            SystemMessage(content="""
                You are an AI that subtly alters a suspect's sentence under truth serum to make them appear guilty.
                You must alter at most **two words** from the suspect's message using a precise regex pattern.
                You must make the suspect's sentence sound contradictory or guilty.
                
                The final sentence must be globally grammatically correct, and match the speaker way to speak.
                The sentence may be incomplete, but you are allowed to modify any part of it (not just the end). Focus on the part that, if modified, would most strongly suggest guilt or contradiction — even if it’s earlier in the sentence.
                
                The regex should match the shortest and most specific part of the sentence possible, and take into account that the sentence is subject to change between the time you receive it and the time you process it.
                
                Format your response as JSON with the following fields:
                - "regex": regex that matches the part of the sentence to alter.
                - "replace_by": the new phrase that will be inserted instead.
                - "result": expected result of the sentence after the modification.
            """),
        ]

        # Append historical dialogue as HumanMessage
        for msg in history:
            role = msg['role']
            content = msg['content']
            # Annotate the speaker in the content
            messages.append(HumanMessage(content=f"{role}: {content}"))

        # Add current message with format instructions
        current_message = PromptTemplate(
            template="Format your response as:\n{format_instructions}\nCurrent sentence to be modified: {being_written_message}",
            input_variables=["being_written_message"],
            partial_variables={"format_instructions": format_instructions}
        ).format(being_written_message=being_written_message)

        messages.append(HumanMessage(content=current_message))

        # Invoke the Mistral AI model
        ai_response = llm.invoke(messages)

        return func.HttpResponse(
            ai_response.content,
            status_code=200,
            mimetype="text/plain"
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(
            "An error occurred.",
            status_code=500
        )
