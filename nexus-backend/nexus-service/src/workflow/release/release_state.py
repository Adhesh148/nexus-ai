from typing import List, Dict
from typing_extensions import TypedDict

# Define State of Workflow Graph
class ReleaseGraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
    """
    release_name: str
    project_id: str
    template_id: str
    issues: List[dict]
    required_fields_info: str
    gathered_info: dict
    combined_info: str
    generated_release_note: str