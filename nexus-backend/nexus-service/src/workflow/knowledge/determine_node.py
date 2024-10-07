from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from config.model_config import create_chat_model

# LLM
llm = create_chat_model()

# prompt
DETERMINE_TEMPLATE = """
You are provided with a list of files, as well as the current chat history. Your task is to determine whether the user query 
is explicitly referencing one or more of the given files.

1. If the query explicitly mentions or clearly refers to any of the provided files, return "YES" followed by a JSON list of the mentioned files.
2. If it is not clear that the query is referencing any of the provided files, return "NO".

User Query: {user_query}

Input Files: {input_files}

Chat history: {chat_history}

Examples:

Example - 1:
User Query: "Can you summarize the key points from the project report?"

Input Files: [resume.pdf, project_report.docx, financial_data.xlsx]

Chat History: []

Output:
```json
{{
  "response": "YES",
  "files": ["project_report.docx"]
}}
```

Example - 2:
User Query: "Can you summarize the key points from the documents"

Input Files: [resume.pdf, project_report.docx, financial_data.xlsx]

Chat History: 
[
    {{
        "input": "Do you have access to the  project report and financial data from knowledge base?"
    }}
]

Output:
```json
{{
  "response": "YES",
  "files": ["project_report.docx", "financial_data.xlsx"]
}}
```

Example - 3:
User Query: "Can you transalate document to french"

Input Files: [resume.pdf, project_report.docx, financial_data.xlsx]

Chat History: []

Output:
```json
{{
  "response": "NO",
}}
```
"""

FILE_RETRIEVER_TEMPLATE = """
You are provided with a list of files, as well as the current chat history. Your task is to get the files which are required by the user query

User Query: {user_query}

Input Files: {input_files}

Chat history: {chat_history}

Examples:

Example - 1:
User Query: "Can you summarize the key points from the project report?"

Input Files: [resume.pdf, project_report.docx, financial_data.xlsx]

Chat History: []

Output:
```json
{{
  "files": ["project_report.docx"]
}}
```

Example - 2:
User Query: "Can you summarize the key points from the documents"

Input Files: [resume.pdf, project_report.docx, financial_data.xlsx]

Chat History: 
[
    {{
        "input": "Do you have access to the  project report and financial data from knowledge base?"
    }}
]

Output:
```json
{{
  "files": ["project_report.docx", "financial_data.xlsx"]
}}
```
"""

def determiner_chain():
    prompt = PromptTemplate(template=DETERMINE_TEMPLATE, input_variables=["user_query", "input_files", "chat_history"])

    determiner = prompt | llm | JsonOutputParser()
    return determiner

def files_retriever_chain():
    prompt = PromptTemplate(template=FILE_RETRIEVER_TEMPLATE, input_variables=["user_query", "input_files", "chat_history"])

    files_retriever = prompt | llm | JsonOutputParser()
    return files_retriever

