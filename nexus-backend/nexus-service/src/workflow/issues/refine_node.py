from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from config.model_config import create_chat_model

# LLM
llm = create_chat_model()

# Requirement prompt
template = """
You are an expert in requirements analysis and refinement. Your task is to review and improve the provided list of requirements. 
This involves removing any duplicate requirements, critiquing each requirement for completeness and clarity, improving the descriptions, 
and filling in any missing details. Additionally, re-estimate the priority if necessary.

Given the initial list of requirements:
-------
{requirements_list}
-------

1. **Remove Duplicates**: Identify and remove any duplicate requirements from the list.
2. **Critique**: For each requirement, assess and critique its completeness and clarity. Provide suggestions for improvement if necessary.
3. **Improve**: Refine each requirement to ensure it is clear, detailed, and actionable. Fill in any missing details.
4. **Re-estimate**: Re-assess and update the priority of each requirement if needed.

Provide the refined list of requirements in the following JSON format. Only return the json response:

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

prompt = PromptTemplate(template=template, input_variables=["requirements_list"])

refinement_chain = prompt | llm | JsonOutputParser()