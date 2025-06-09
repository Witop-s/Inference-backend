import json
import re
from langchain_core.runnables import RunnableMap, RunnableLambda
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_openai import OpenAI
from langchain.chat_models import init_chat_model
from prompts.prompt_alteration import alteration_prompt, output_parser, format_instructions

# Modèle
# llm = ChatMistralAI(model="mistral-large-latest", temperature=0.2, max_retries=2)
# llm = init_chat_model("gpt-4.1-mini", model_provider="openai")
llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai", temperature=0.2, max_retries=2)

def log_input_to_llm(x):
    print("\n📨 Prompt sent to LLM:\n")
    if isinstance(x, dict):
        for k, v in x.items():
            print(f"--- {k} ---\n{v}\n")
    else:
        print(x)
    return x
log_input = RunnableLambda(log_input_to_llm)

def log_output_from_llm(x):
    print("\n📬 Response from LLM:\n")
    if hasattr(x, "content"):
        print(x.content)
    else:
        print(str(x))
    return x
log_output = RunnableLambda(log_output_from_llm)

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
            "format_instructions": lambda _: format_instructions
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
