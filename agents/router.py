def route(state):
    query = state["query"]

    if state.get("vector_store"):
        return "rag"

    return "general"