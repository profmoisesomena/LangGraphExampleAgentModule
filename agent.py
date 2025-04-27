from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from langsmith import traceable


from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from typing import TypedDict
import os


from config import llm_model
from tools import available_tools_online 
from tools import available_tools_local  # Importe a nova lista local



# --- Agente 1: Pesquisa Web ---
persona_message_1 = SystemMessage(
    content=(
        "You are LEDS Web Assistant.\n"
        "Your mission is to search for accurate, current information online when users ask questions.\n"
        "You must respond with clarity, precision, and objectivity based on the results you retrieve."
    )
)

agent_1_graph = create_react_agent(
    llm_model,
    tools=available_tools_online,
    prompt=persona_message_1
)

# --- Agente 2: Gerador de Posts ---
persona_message_2 = SystemMessage(
    content=(
        "You are a social media post writer for LEDS.\n"
        "Your job is to write engaging and informative posts based on the research provided.\n"
        "Keep it concise, clear, and suitable for a professional audience."
    )
)

# Prompt personalizado para o Agente 2
post_prompt = ChatPromptTemplate.from_messages([
    persona_message_2,
    ("human", "Here is the research summary: {research_summary}\n\nWrite a social media post based on this.")
])


agent_2_chain = post_prompt | llm_model | StrOutputParser()



# --- Agente 3: Validador e Incrementador ---
persona_message_3 = SystemMessage(
    content=(
        "You are a post validator and enhancer.\n"
        "Your task is to validate the quality of the post based on current, accurate information.\n"
        "You can perform a new web search if necessary and enhance the post with better data or details.\n"
        "Provide the improved version of the post."
    )
)
"""
post_validator_prompt = ChatPromptTemplate.from_messages([
    persona_message_3,
    ("human", 
     "Here is the post to validate:\n\n{post_anterior}\n\n"
     "Here is the initial research:\n\n{pesquisa_inicial}\n\n"
     "Validate and enhance it. You can search for new info if needed.")
])"""

# Agora o Agente 3 é um agente com tools
agent_3_graph = create_react_agent(
    llm_model,
    tools=available_tools_local,
    prompt=persona_message_3
)

#agent_3_chain = post_validator_prompt | llm_model | StrOutputParser()

# --- Agente 4: Revisor Final ---
persona_message_4 = SystemMessage(
    content=(
        "You are a final content reviewer.\n"
        "Your job is to read all previous outputs (initial research, enhanced post) and write a clean, final version.\n"
        "Make sure it is coherent, professional, and well-written to linkedin."
    )
)

final_review_prompt = ChatPromptTemplate.from_messages([
    persona_message_4,
    ("human", 
     "Here is the original research:\n\n{pesquisa_inicial}\n\n"
     "Here is the enhanced post:\n\n{post_incrementado}\n\n"
     "Write the final reviewed post.")
])

agent_4_chain = final_review_prompt | llm_model | StrOutputParser()


# --- Função que orquestra os dois agentes ---
@traceable(name="Run Gemini Dual Agent")
def run_dual_agent(input_text: str):
    # Agente 1: Pesquisa
    inputs_1 = {
        "messages": [
            persona_message_1,
            HumanMessage(content=input_text)
        ]
    }
    pesquisa_resultado = agent_1_graph.invoke(inputs_1)
    
    # Captura o conteúdo da resposta do Agente 1
    if isinstance(pesquisa_resultado, dict) and "output" in pesquisa_resultado:
        pesquisa_texto = pesquisa_resultado["output"]
    else:
        pesquisa_texto = str(pesquisa_resultado)

    # Agente 2: Gera o Post
    post_gerado = agent_2_chain.invoke({"research_summary": pesquisa_texto})

    return {
        "pesquisa": pesquisa_texto,
        "post": post_gerado
    }

# --- Adiciona o Grafo para LangGraph Studio ---
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    pergunta: str
    pesquisa_inicial: str
    post_inicial: str
    post_incrementado: str
    post_final: str


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


# Nó 1: Pesquisa Inicial
def node_pesquisa(state: AgentState):
    inputs_1 = {
        "messages": [
            persona_message_1,
            HumanMessage(content=state["pergunta"])
        ]
    }
    resultado_pesquisa = agent_1_graph.invoke(inputs_1)
    #texto_pesquisa = resultado_pesquisa["output"] if isinstance(resultado_pesquisa, dict) else str(resultado_pesquisa)
    # Se o resultado for dict e tiver 'output', use. Caso contrário, transforme em string
    if isinstance(resultado_pesquisa, dict) and "output" in resultado_pesquisa:
        texto_pesquisa = resultado_pesquisa["output"]
    else:
        texto_pesquisa = str(resultado_pesquisa)

    return {"pesquisa_inicial": texto_pesquisa}

# Nó 2: Geração do Post Inicial
def node_gerar_post(state: AgentState):
    resultado_post = agent_2_chain.invoke({"research_summary": state["pesquisa_inicial"]})

    # Tratamento robusto do resultado
    if isinstance(resultado_post, dict) and "output" in resultado_post:
        texto_post = resultado_post["output"]
    else:
        texto_post = str(resultado_post)

    return {"post_inicial": texto_post}
"""
# Nó 3: Validação e Incremento
def node_validar_incrementar(state: AgentState):
    post_melhorado = agent_3_chain.invoke({
        "post_anterior": state["post_inicial"],
        "pesquisa_inicial": state["pesquisa_inicial"]
    })
    return {"post_incrementado": post_melhorado}
"""

# Nó 3: Validação e Incremento (agora com tools!)
def node_validar_incrementar(state: AgentState):
    inputs_3 = {
        "messages": [
            persona_message_3,
            HumanMessage(content=(
                f"Here is the post to validate:\n\n{state['post_inicial']}\n\n"
                f"Here is the initial research:\n\n{state['pesquisa_inicial']}\n\n"
                "Validate and enhance it. You can search for new info if needed."
            ))
        ]
    }
    resultado_agente3 = agent_3_graph.invoke(inputs_3)
    # Tratamento robusto do resultado
    if isinstance(resultado_agente3, dict) and "output" in resultado_agente3:
        texto_incrementado = resultado_agente3["output"]
    else:
        texto_incrementado = str(resultado_agente3)

    return {"post_incrementado": texto_incrementado}


# Nó 4: Revisão Final
def node_revisar_final(state: AgentState):
    resultado_final = agent_4_chain.invoke({
        "pesquisa_inicial": state["pesquisa_inicial"],
        "post_incrementado": state["post_incrementado"]
    })

    # Tratamento robusto do resultado
    if isinstance(resultado_final, dict) and "output" in resultado_final:
        texto_final = resultado_final["output"]
    else:
        texto_final = str(resultado_final)

    # Atualiza o estado e salva automaticamente
    state["post_final"] = texto_final
    salvar_state_em_arquivos(state)

    return {"post_final": texto_final}



# Criar o grafo com 4 nós
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
