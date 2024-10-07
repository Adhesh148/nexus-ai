from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from config.model_config import create_chat_model

# LLM
llm = create_chat_model()

# Requirement prompt
template = """
You are an expert tasked with extracting actionable requirements from a document. The extracted information will be used to create Jira issues for a 
software development project.

Given the document content:
-------
{document_content}
-------

Identify and list the requirements in a structured format. Each requirement should include a summary, any relevant details, and 
additional considerations such as risks, assumptions, and dependencies.

Provide the output in the following JSON format. Only return the json response:

```json
{{
    "requirements": [
        {{
            "summary": "<summary of the requirement>",
            "description": "<description of the requirement>",
            "priority": "<low/medium/high>",
            "issue_type": "<bug/story/task>",
            "story_points": "number that represents JIRA based story point estimation"
            "additional_considerations": {{
                "acceptance criteria": "any acceptance criteria",
                "risks": "any identified risks",
                "assumptions": "key assumptions",
                "dependencies": "dependencies"
            }}
        }},
        ...
    ]
}}
```
"""

prompt = PromptTemplate(template=template, input_variables=["document_content"])

requirement_gatherer = prompt | llm | JsonOutputParser()