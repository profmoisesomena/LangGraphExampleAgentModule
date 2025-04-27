from langgraph.prebuilt import create_react_agent
from config import llm_model
from tools import available_tools_online, available_tools_local
from agents.personas import persona_message_1, persona_message_3

# Agente 1: Pesquisa Web
agent_1_graph = create_react_agent(
    llm_model,
    tools=available_tools_online,
    prompt=persona_message_1
)

# Agente 3: Validador com tools locais
agent_3_graph = create_react_agent(
    llm_model,
    tools=available_tools_local,
    prompt=persona_message_3
)
