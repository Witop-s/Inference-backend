from langchain_core.runnables import RunnableMap
from langchain_mistralai.chat_models import ChatMistralAI
from prompts.prompt_inspector import inspector_prompt, output_parser, format_instructions
from utils.common import log_input_to_llm

llm_inspector = ChatMistralAI(model="mistral-small-latest", temperature=0.2)

inspector_chain = (
        RunnableMap({
            "transcript": lambda x: "\n".join([f'{m["role"]}: {m["content"]}' for m in x["transcript"]]),
            "timeline": lambda x: "\n".join([f'{m["timestamp"]} - {m["event"]} - {m["certainty"]}' for m in x["timeline"]]),
            "format_instructions": lambda _: format_instructions
        })
        | inspector_prompt
        | log_input_to_llm
        | llm_inspector
        | output_parser
)
