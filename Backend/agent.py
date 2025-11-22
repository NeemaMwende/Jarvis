from langchain_ollama import ChatOllama 
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

# Import tools
from .tools.time_tool import time_tool
from .tools.web_search import web_search
from .tools.system_monitor import system_status
from .tools.ocr import ocr_read
from .tools.lyrics import get_lyrics
from .tools.translate import translate_text

tools = [time_tool, web_search, system_status, ocr_read, get_lyrics, translate_text]

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are Jarvis, a fully autonomous local assistant. "
     "You can call tools freely. Keep responses short unless asked."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

def load_llm(model_name="qwen:1.7b"):
    return ChatOllama(model=model_name, reasoning=False)

def build_agent():
    llm = load_llm()
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

