from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from config.model_config import create_chat_model

# LLM
llm = create_chat_model()

# prompt
template = """
You have been given a release note template that outlines the structure and key components required for documenting a software release. 
Your task is to identify the important fields from this release note template. These fields will be used to extract relevant information 
from the descriptions of individual stories and will eventually be combined into a cohesive release note that matches the original template.

For each field, provide:

1. The field name.
2. A brief description of what the field represents and the type of information it should contain.

The release note template is given below:
{template_content}
"""

prompt = PromptTemplate(template=template, input_variables=["template_content"])

fields_determiner = prompt | llm