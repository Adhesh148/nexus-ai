from langgraph.graph import END, StateGraph, START
from workflow.knowledge.knowledge_state import KnowledgeGraphState
from workflow.knowledge.knowledge_nodes import file_retriever_node, direct_query, vector_query, determine_edge
from langchain.memory import ConversationBufferMemory

from pprint import pprint

def route_decision(state, result):
    # Update the state with any additional information
    for key, value in result.items():
        if key != "decision":
            state[key] = value
    # Return the decision
    return result["decision"]

workflow = StateGraph(KnowledgeGraphState)

# Define the nodes
workflow.add_node("file_retriever", file_retriever_node)
workflow.add_node("direct_query", direct_query)
workflow.add_node("vector_query", vector_query)

# Build graph
workflow.add_conditional_edges(
    START,
    determine_edge,
    {
        "direct_query": "file_retriever",
        "vector_query": "vector_query",
    }
)
workflow.add_edge("file_retriever", "direct_query")

# Compile
knowledge_graph = workflow.compile()

if __name__ == "__main__":
    inputs = {"project_id": "101", "user_query": "Summarize contents of requirment_test.txt", "chat_history": ConversationBufferMemory()}

    for output in knowledge_graph.stream(inputs):
        for key, value in output.items():
            pass
    
    result = value["result"]
    pprint(result)