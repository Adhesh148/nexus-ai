from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from config.model_config import create_chat_model

# LLM
llm = create_chat_model()

# Requirement prompt
template = """
You are an AI assistant tasked with extracting relevant information from issue summaries and descriptions to populate a release note. 
You will be provided with the summary and description of an issue or story. Your job is to analyze this information and extract details that contain
information relevant to each field given.

For each field, provide the extracted information if applicable. If no relevant information is found for a field, leave it blank. Do not make up information.
-------
Issue Information is given below:
{issue_input}

The fields to be extracted are given below:
{fields_info}
"""

prompt = PromptTemplate(template=template, input_variables=["issue_input", "fields_info"])

gatherer = prompt | llm