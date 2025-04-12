# Importações necessárias para configuração do agente inteligente
import os
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults

# Carregar variáveis de ambiente (.env)
load_dotenv()

# Configuração das APIs
GEMINI_TOKEN = os.getenv("GEMINI_API_KEY")
TAVILY_TOKEN = os.getenv("TAVILY_API_KEY")

# Instanciação do modelo LLM da Google
llm_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    api_key=GEMINI_TOKEN
)

# Definição da personalidade do agente via SystemMessage
persona_message = SystemMessage(
    content=(
        "You are LEDS Web Assistant.\n"
        "Your mission is to search for accurate, current information online when users ask questions.\n"
        "You must respond with clarity, precision, and objectivity based on the results you retrieve."
    )
)

# Definição da ferramenta de busca web
@tool
def online_lookup(prompt: str = "") -> str:
    """
    Execute a web search based on the provided user prompt.
    Returns summarized relevant information.
    Maximum of 4 curated results using Tavily API.
    """
    search_client = TavilySearchResults(max_results=4, api_key=TAVILY_TOKEN)
    results = search_client.invoke(prompt)
    return results

# Lista de ferramentas disponíveis para o agente
available_tools = [online_lookup]

# Criação do agente de raciocínio e ação baseado no modelo LLM + ferramentas
agent_graph = create_react_agent(
    llm_model,
    tools=available_tools,
    prompt=persona_message
)
