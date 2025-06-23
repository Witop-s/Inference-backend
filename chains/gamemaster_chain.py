from langchain_core.runnables import RunnableMap
from langchain_mistralai.chat_models import ChatMistralAI
from prompts.prompt_gamemaster import gamemaster_prompt, format_instructions

from models.gamemaster_model import JsonOutput
from utils.common import log_input_to_llm, log_output_from_llm

llm_inspector = ChatMistralAI(model_name="mistral-small-latest", temperature=0.2, timeout=9999, max_retries=2)

gamemaster_chain = (
        RunnableMap({
            "game_data": lambda x: x,
            "format_instructions": lambda _: format_instructions
        })
        | gamemaster_prompt
        | log_input_to_llm
        | llm_inspector.with_structured_output(JsonOutput)
        | log_output_from_llm
)
