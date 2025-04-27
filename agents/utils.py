import os
from agents.state import AgentState  # Corrigir import

def salvar_state_em_arquivos(state: AgentState, pasta_destino: str = "resultados"):
    # Garante que a pasta exista
    os.makedirs(pasta_destino, exist_ok=True)

    # Salvar cada parte como .txt
    with open(os.path.join(pasta_destino, "pesquisa_inicial.txt"), "w", encoding="utf-8") as f:
        f.write(state["pesquisa_inicial"])

    with open(os.path.join(pasta_destino, "post_inicial.txt"), "w", encoding="utf-8") as f:
        f.write(state["post_inicial"])

    with open(os.path.join(pasta_destino, "post_incrementado.txt"), "w", encoding="utf-8") as f:
        f.write(state["post_incrementado"])

    # Salvar o resultado final como Markdown
    markdown_content = f"# Post Final Revisado\n\n{state['post_final']}\n"
    with open(os.path.join(pasta_destino, "post_final.md"), "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"Arquivos salvos em: {pasta_destino}")
