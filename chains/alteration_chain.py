import re
from langchain_core.runnables import RunnableMap, RunnableLambda
from langchain_mistralai.chat_models import ChatMistralAI
from prompts.prompt_alteration import alteration_prompt, output_parser, format_instructions

# Modèle
llm = ChatMistralAI(model="mistral-large-latest", temperature=0.2, max_retries=2)

def log_input_to_llm(x):
    print("\n📨 Prompt sent to LLM:\n")
    if isinstance(x, dict):
        for k, v in x.items():
            print(f"--- {k} ---\n{v}\n")
    else:
        print(x)
    return x
log_input = RunnableLambda(log_input_to_llm)

clean_output = RunnableLambda(lambda x: clean_markdown_blocks(x))

prompt_node = (
        RunnableMap({
            "being_written_message": lambda x: x["being_written_message"],
            "history": lambda x: "\n".join([f'{m["role"]}: {m["content"]}' for m in x["history"]]),
            "format_instructions": lambda _: format_instructions,
        })
        | alteration_prompt
)

# Chaîne
inner_voice_chain = (
        prompt_node
        | log_input
        | llm
        | clean_output
        | output_parser
)

def clean_markdown_blocks(raw):
    if hasattr(raw, "content"):
        text = raw.content
    else:
        text = str(raw)

    # Supprime les blocs ```json ... ```
    cleaned = re.sub(r"^```json\s*|```$", "", text.strip(), flags=re.MULTILINE)
    return cleaned
