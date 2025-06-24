from langchain_core.runnables import RunnableMap
from langchain_mistralai.chat_models import ChatMistralAI

from prompts.prompt_fact_filter import fact_filter_prompt

llm_filter = ChatMistralAI(model="mistral-small-latest", temperature=0.2)

select_facts_chain = (
        RunnableMap({
            "facts": lambda x: x["facts"],
            "dialogue": lambda x: "\n".join([f'{m["role"]}: {m["content"]}' for m in x["dialogue"]])
        })
        | fact_filter_prompt
        | llm_filter
)
