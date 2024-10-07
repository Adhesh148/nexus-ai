from langgraph.graph import END, StateGraph, START
from workflow.issues.issue_state import IssueGraphState
from workflow.issues.issue_nodes import load, gather_requirements, refine_requirements

from pprint import pprint

workflow = StateGraph(IssueGraphState)

# Define the nodes
workflow.add_node("load", load)
workflow.add_node("gather", gather_requirements)
workflow.add_node("refine", refine_requirements)

# Build graph
workflow.add_edge(START, "load")
workflow.add_edge("load", "gather")
workflow.add_edge("gather", "refine")

# Compile
issue_graph = workflow.compile()

if __name__ == "__main__":
    inputs = {"file_ids": ["2c3fc75a-50e7-482f-8411-17569c0fc08d"]}

    for output in issue_graph.stream(inputs):
        for key, value in output.items():
            # Node
            pprint(f"Node '{key}':")
            # Optional: print full state at each node
            # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
        pprint("\n---\n")
    
    req = value["requirements"]
    for item in req:
        pprint(f"Requirements: {item['summary']}")
