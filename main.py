from agents.graph_builder import agent_graph
from agents.graph_builder import AgentState

if __name__ == "__main__":
    # Entrada inicial para o grafo
    entrada = AgentState(pergunta="O que é o Protocolo A2A e qual sua integração com Langgraph?")

    # Executar o grafo com a entrada
    resultado_final = agent_graph.invoke(entrada)

    # Exibir resultado final no terminal
    print("\n--- Resultado Final ---\n")
    print(resultado_final["post_final"])