import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.graph import build_graph

graph = build_graph()

def handle_chat(user, query, vector_store=None):
    state = {
        "query": query,
        "vector_store": vector_store
    }

    result = graph.invoke(state)
    response = result["response"]

    return response  