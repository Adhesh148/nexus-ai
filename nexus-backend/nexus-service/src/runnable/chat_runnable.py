from datetime import date
from typing import List, Optional, Dict, Any
import logging
from collections import defaultdict
from operator import itemgetter

from langchain_core.runnables import RunnablePassthrough, RunnableSerializable, RunnableConfig, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain_core.tools import BaseTool
from langchain.agents.format_scratchpad import format_to_tool_messages
from langchain.agents.output_parsers import ToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_core.runnables.utils import ConfigurableFieldSpec
from langchain_core.language_models import BaseChatModel
from langchain.memory import ConversationBufferMemory

from prompts.chat_prompts import DEFAULT_SYSTEM_PROMPT
from config.model_config import create_chat_model
from tools.confluence_tool import ConfluenceTool
from tools.sample_tool import CustomSearchTool
from tools.knowledge_base_tool import KnowledgeBaseTool
from tools.code_retriever_tool import CodeRetrieverTool

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def memory_factory():
    return ConversationBufferMemory(memory_key="chat_history", k=12, input_key="user", return_messages=True)

class ChatRunnable(RunnableSerializable):
    """A configurable chat runnable compatible with LangServe."""

    tools: List[BaseTool] = []
    agent: Any = None
    agent_executor: AgentExecutor = None
    current_session_id: Optional[str] = None
    current_project_id: Optional[str] = None
    prompt: ChatPromptTemplate = None
    model: BaseChatModel = None
    chat_history: Dict[str, ConversationBufferMemory] = defaultdict(memory_factory)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self):
        super().__init__()
        self.prompt = self._create_prompt()
        self.model = create_chat_model()

    def _create_prompt(self):
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate(
                    prompt=PromptTemplate(
                        input_variables=["user"], # fill in project name later
                        template=DEFAULT_SYSTEM_PROMPT,
                        partial_variables={"today": date.today().strftime("%B %d %Y")}
                    ),                    
                ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

    def _create_agent(self, tools, memory: ConversationBufferMemory):
        model_with_tools = self.model.bind_tools(tools)
        return (
            RunnablePassthrough.assign(
                agent_scratchpad=lambda x: format_to_tool_messages(x["intermediate_steps"])
            ) |
            RunnablePassthrough.assign(
                history=RunnableLambda(
                    memory.load_memory_variables) | itemgetter("chat_history")
            )
            | self.prompt | model_with_tools | ToolsAgentOutputParser()
        )

    def _get_project_tools(self, session_id: str, project_id: str, memory: ConversationBufferMemory) -> List[BaseTool]:
        logger.info(f"Loading project tools for project ID: {project_id} and session: {session_id}")
        if project_id == "101":
            return [
                ConfluenceTool(session_id=session_id, project_id=project_id).as_tool(),
                KnowledgeBaseTool(session_id=session_id, project_id=project_id, memory=memory).as_tool(),
                CodeRetrieverTool(session_id=session_id, project_id=project_id, memory=memory).as_tool(),
            ]
        else:
            return [CustomSearchTool().as_tool()]

    def _reconfigure(self, session_id: str, project_id: str):
        logger.info(f"Reconfiguring for session ID: {session_id}, project ID: {project_id}")
        memory = self.chat_history[session_id]
        all_tools = self.tools + self._get_project_tools(session_id, project_id, memory)
        self.agent = self._create_agent(all_tools, memory)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=all_tools, verbose=True, memory=memory)
        self.current_session_id = session_id
        self.current_project_id = project_id
        logger.info(f"Reconfigured with {len(all_tools)} tools")

    def invoke(self, input: Dict[str, Any], config: Optional[RunnableConfig] = None) -> Dict[str, Any]:
        config = config or {}
        session_id = config.get("configurable", {}).get("session_id", "")
        project_id = config.get("configurable", {}).get("project_id", "")

        # Reconfigure if necessary
        self._reconfigure(session_id, project_id)

        # Add user to the input if provided in config
        input["user"] = config.get("configurable", {}).get("user", "default_user")

        # invoke model
        result = self.agent_executor.invoke(input)

        # Update chat history
        self.chat_history[session_id].chat_memory.add_user_message(input["input"])
        self.chat_history[session_id].chat_memory.add_ai_message(result["output"])

        return result
    
    @property
    def config_specs(self) -> List[ConfigurableFieldSpec]:
        return [
            ConfigurableFieldSpec(
                id="session_id",
                annotation=str,
                name="Session ID",
                description="Unique identifier for the chat session",
                default=""
            ),
            ConfigurableFieldSpec(
                id="project_id",
                annotation=str,
                name="Project ID",
                description="Unique identifier for the project",
                default=""
            ),
            ConfigurableFieldSpec(
                id="memory",
                annotation=str,
                name="Chat History",
                description="Chat history",
                default=""
            ),
            ConfigurableFieldSpec(
                id="user",
                annotation=str,
                name="User",
                description="User identifier",
                default="default_user"
            )
        ]