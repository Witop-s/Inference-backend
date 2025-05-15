import logging
import azure.functions as func
from dotenv import load_dotenv
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# Initialize the Mistral AI model
llm = ChatMistralAI(
    model="mistral-large-latest",  # You can choose other available models
    temperature=0.7,
    max_retries=2
)

# Define the schema
response_schemas = [
    ResponseSchema(name="to_insert", description="The text to insert"),
    ResponseSchema(name="instead_of", description="The text to be replaced")
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

app = func.FunctionApp()

@app.route(route="inner-voice", auth_level=func.AuthLevel.ANONYMOUS)
def inner_voice(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body_json = req.get_json()
        being_written_message = body_json['being_written_message']
        history = body_json['history']

        print(being_written_message)
        print(history)

        # Prepare the message sequence
        messages = [
            SystemMessage(content="The player has been affected by a truth serum and is being questioned by an inspector. You replace part of their speach with compromising information. You can only replace/delete/add a maximum of 2 words.)"),
        ]

        # Append historical dialogue as HumanMessage
        for msg in history:
            role = msg['role']
            content = msg['content']
            # Annotate the speaker in the content
            messages.append(HumanMessage(content=f"{role}: {content}"))

        # Add current message with format instructions
        current_message = PromptTemplate(
            template="Format your response as:\n{format_instructions}\nCurrent thought: {being_written_message}",
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