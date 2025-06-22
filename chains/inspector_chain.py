from langchain_core.runnables import RunnableMap
from langchain_mistralai.chat_models import ChatMistralAI
from prompts.prompt_inspector import inspector_prompt, InspectorOutput, format_instructions
from utils.common import log_input_to_llm, log_output_from_llm

llm_inspector = ChatMistralAI(model_name="mistral-large-latest", temperature=0.2, timeout=9999, max_retries=2)

inspector_chain = (
        RunnableMap({
            "dialogue": lambda x: "\n".join([f'{m["role"]}: {m["content"]}' for m in x["dialogue"]]),
            "scenario": lambda x: x["scenario"],
            "format_instructions": lambda _: format_instructions
        })
        | inspector_prompt
        | log_input_to_llm
        | llm_inspector.with_structured_output(InspectorOutput)
        | log_output_from_llm
)
