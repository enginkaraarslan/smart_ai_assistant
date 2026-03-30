def evaluate(state):
    response = state["response"]

    if len(response) < 20:
        state["quality"] = "Low"
    else:
        state["quality"] = "Good"

    return state