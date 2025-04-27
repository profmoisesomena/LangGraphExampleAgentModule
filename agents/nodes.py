from langchain_core.messages import HumanMessage
from agents.create_agents import agent_1_graph, agent_3_graph
from agents.chains import agent_2_chain, agent_4_chain
from agents.personas import persona_message_1, persona_message_3
from agents.utils import salvar_state_em_arquivos

# Node 1: Initial Research
def node_pesquisa(state):
    inputs_1 = {"messages": [persona_message_1, HumanMessage(content=state["pergunta"])]}
    resultado = agent_1_graph.invoke(inputs_1)
    # Se o resultado for dict e tiver 'output', use. Caso contrário, transforme em string
    if isinstance(resultado, dict) and "output" in resultado:
        texto = resultado["output"]
    else:
        texto = str(resultado)

    return {"pesquisa_inicial": texto}

# Node 2: Initial Post Generation
def node_gerar_post(state):
    resultado = agent_2_chain.invoke({"research_summary": state["pesquisa_inicial"]})
    
    if isinstance(resultado, dict) and "output" in resultado:
        texto_post = resultado["output"]
    else:
        texto_post = str(resultado)

    return {"post_inicial": texto_post}

# Node 3: Validation and Incrementation (with local tools!)
def node_validar_incrementar(state):
    inputs_3 = {"messages": [
        persona_message_3,
        HumanMessage(content=(
            f"Here is the post to validate:\n\n{state['post_inicial']}\n\n"
            f"Here is the initial research:\n\n{state['pesquisa_inicial']}\n\n"
            "Validate and enhance it. You can search for new info if needed."
        ))
    ]}
    resultado = agent_3_graph.invoke(inputs_3)
    
    if isinstance(resultado, dict) and "output" in resultado:
        texto = resultado["output"]
    else:
        texto = str(resultado)

    return {"post_incrementado": texto}

# Node 4: Final Review
def node_revisar_final(state):
    resultado = agent_4_chain.invoke({
        "pesquisa_inicial": state["pesquisa_inicial"],
        "post_incrementado": state["post_incrementado"]
    })

    if isinstance(resultado, dict) and "output" in resultado:
        texto = resultado["output"]
    else:
        texto = str(resultado)

    state["post_final"] = texto
    salvar_state_em_arquivos(state)
    return {"post_final": texto}
