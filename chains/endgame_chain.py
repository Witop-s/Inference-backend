from langchain_core.runnables import RunnableMap
from langchain_mistralai.chat_models import ChatMistralAI

from prompts.prompt_endgame import endgame_prompt, format_instructions

llm_endgame = ChatMistralAI(model="mistral-small-latest", temperature=0.2)

endgame_chain = (
        RunnableMap({
            "game_data": lambda x: x,
            "format_instructions": lambda _: format_instructions
        })
        | endgame_prompt
        | llm_endgame
)
