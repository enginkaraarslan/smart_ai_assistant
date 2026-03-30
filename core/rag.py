from core.llm import get_llm

def rag_answer(query, docs):
    model = get_llm()

    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a professional AI assistant.

Use ONLY the given context to answer.

Context:
{context}

Question:
{query}

Give structured answer with headings.
"""

    response = model.generate_content(prompt)
    return response.text