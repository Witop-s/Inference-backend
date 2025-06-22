from langchain_core.runnables import RunnableLambda


def log_input_to_llm(x):
    print("\n📨 Prompt sent to LLM:\n")
    if isinstance(x, dict):
        for k, v in x.items():
            print(f"--- {k} ---\n{v}\n")
    else:
        print(x)
    print("\n--- End of Prompt ---\n")
    return x
log_input = RunnableLambda(log_input_to_llm)

def log_output_from_llm(x):
    print("\n📬 Response from LLM:\n")
    if hasattr(x, "content"):
        print(x.content)
    else:
        print(str(x))
    print("\n--- End of Response ---\n")
    return x
log_output = RunnableLambda(log_output_from_llm)