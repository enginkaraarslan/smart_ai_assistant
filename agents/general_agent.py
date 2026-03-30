from services.prompts import get_system_prompt
from core.llm import get_llm

llm = get_llm()

def run_general(state):
    query = state["query"]

    prompt = f"""
{get_system_prompt()}

User Question:
{query}
"""

    result = llm.generate_content(prompt)

    state["response"] = result.text
    return state