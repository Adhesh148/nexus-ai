from langgraph.graph import END, StateGraph, START
from workflow.release.release_state import ReleaseGraphState
from workflow.release.release_nodes import load, gather, combine, refine, determine_fields
import markdown

from pprint import pprint

workflow = StateGraph(ReleaseGraphState)

# Define the nodes
workflow.add_node("load", load)
workflow.add_node("determine", determine_fields)
workflow.add_node("gather", gather)
workflow.add_node("combine", combine)
workflow.add_node("refine", refine)

# Build graph
workflow.add_edge(START, "load")
workflow.add_edge("load", "determine")
workflow.add_edge("determine", "gather")
workflow.add_edge("gather", "combine")
workflow.add_edge("combine", "refine")

# Compile
release_graph = workflow.compile()

if __name__ == "__main__":
    inputs = {"release_name": "release/0.1.0", "project_id": "101", "template_id": "96e256b2-65e0-4fce-b96b-e1affe631447"}

    for output in release_graph.stream(inputs):
        for key, value in output.items():
            # Node
            pprint(f"Node '{key}':")
            # Optional: print full state at each node
            # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
        pprint("\n---\n")
    
    response = value["generated_release_note"]
    pprint(response)
    html_content = markdown.markdown(response, extensions=['extra'])
    pprint(html_content)
