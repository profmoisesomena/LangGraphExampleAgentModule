from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents.nodes import node_pesquisa, node_gerar_post, node_validar_incrementar, node_revisar_final
from agents.state import AgentState 

builder = StateGraph(AgentState)
builder.add_node("pesquisa_web", node_pesquisa)
builder.add_node("gerar_post", node_gerar_post)
builder.add_node("validar_incrementar", node_validar_incrementar)
builder.add_node("revisar_final", node_revisar_final)

builder.set_entry_point("pesquisa_web")
builder.add_edge("pesquisa_web", "gerar_post")
builder.add_edge("gerar_post", "validar_incrementar")
builder.add_edge("validar_incrementar", "revisar_final")
builder.add_edge("revisar_final", END)

agent_graph = builder.compile()




