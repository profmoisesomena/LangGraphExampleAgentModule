from agent import run_dual_agent

if __name__ == "__main__":
    resultado = run_dual_agent("O que é o Protocolo A2A e qual sua integração com Langgraph?")
    print("\n--- Pesquisa ---\n")
    print(resultado["pesquisa"])
    print("\n--- Post Gerado ---\n")
    print(resultado["post"])
