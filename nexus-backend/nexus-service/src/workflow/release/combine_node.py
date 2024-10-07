from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from config.model_config import create_chat_model

# LLM
llm = create_chat_model()

# prompt
template = """
You are an AI assistant tasked with compiling and organizing information for a release note. You will be provided with multiple sets of 
extracted information from various issues or stories. Your job is to combine this information while removing any duplicates or redundant entries.
Focus on the fields given while combining the information. Do not make up any information.

The extracted information is given below:
{extracted_info}

The important fields to focus on is given below:
{fields_info}
"""

prompt = PromptTemplate(template=template, input_variables=["extracted_info", "fields_info"])

combiner = prompt | llm