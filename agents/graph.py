from langgraph.graph import StateGraph
from agents.router import route
from agents.rag_agent import run_rag
from agents.general_agent import run_general
from agents.evaluator import evaluate

def build_graph():

    graph = StateGraph(dict)

    graph.add_node("rag", run_rag)
    graph.add_node("general", run_general)
    graph.add_node("eval", evaluate)

    graph.set_conditional_entry_point(
        route,
        {
            "rag": "rag",
            "general": "general"
        }
    )

    graph.add_edge("rag", "eval")
    graph.add_edge("general", "eval")

    return graph.compile()