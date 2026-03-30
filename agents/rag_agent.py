from services.prompts import get_system_prompt
from core.vector_store import retrieve_docs
from core.llm import get_llm

llm = get_llm()

def run_rag(state):
    query = state["query"]
    vector_store = state.get("vector_store")

    docs = retrieve_docs(vector_store, query) if vector_store else []

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
{get_system_prompt()}

Context:
{context}

User Question:
{query}
"""

    result = llm.generate_content(prompt)

    state["response"] = result.text
    return state