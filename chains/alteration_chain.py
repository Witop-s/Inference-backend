import json
import re
from langchain_core.runnables import RunnableMap, RunnableLambda
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_openai import OpenAI
from langchain.chat_models import init_chat_model
from prompts.prompt_alteration import alteration_prompt, output_parser, format_instructions
from utils.common import log_input, log_output

# Modèle
# llm = ChatMistralAI(model="mistral-large-latest", temperature=0.2, max_retries=2)
# llm = init_chat_model("gpt-4.1-mini", model_provider="openai")
llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai", temperature=0.2, max_retries=2)

def clean_markdown_blocks(raw):
    if hasattr(raw, "content"):
        text = raw.content
    else:
        text = str(raw)

    # Supprime les blocs ```json ... ```
    cleaned = re.sub(r"^```json\s*|```$", "", text.strip(), flags=re.MULTILINE)
    return cleaned
clean_output = RunnableLambda(lambda x: clean_markdown_blocks(x))

prompt_node = (
        RunnableMap({
            "being_written_message": lambda x: x["being_written_message"],
            "transcript": lambda x: "\n".join([f'{m["role"]}: {m["content"]}' for m in x["transcript"]]),
            "format_instructions": lambda _: format_instructions,
            "scenario": lambda x: x["scenario"]
        })
        | alteration_prompt
)

# Chaîne
inner_voice_chain = (
        prompt_node
        | log_input
        | llm
        | log_output
        | output_parser
        | log_output
)
