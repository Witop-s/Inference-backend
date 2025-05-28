from langchain_core.runnables import RunnableLambda


def log_input_to_llm(x):
    print("\n📨 Prompt sent to LLM:\n")
    if isinstance(x, dict):
        for k, v in x.items():
            print(f"--- {k} ---\n{v}\n")
    else:
        print(x)
    return x
log_input = RunnableLambda(log_input_to_llm)