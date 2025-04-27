from typing import TypedDict

class AgentState(TypedDict):
    pergunta: str
    pesquisa_inicial: str
    post_inicial: str
    post_incrementado: str
    post_final: str
