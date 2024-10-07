from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from config.model_config import create_chat_model

# LLM
llm = create_chat_model()

# prompt
template = """
You are an AI assistant tasked with compiling and organizing information for a release note. You are provided combined information from
multiple issues/stories. You have to create a release note in the format given the template release note given. Do not make up any information
and strictly use the information available. Only output the final release note. Do not return any system reponse. 
Return the release note in HTML embedded markdown format.

The combined information is given below:
{combined_info}

The sample template is given below:
{template_content}
"""

prompt = PromptTemplate(template=template, input_variables=["combined_info", "template_content"])

refiner = prompt | llm