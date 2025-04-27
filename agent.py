from langsmith import traceable
from agents.graph_builder import agent_graph
@traceable(name="Full Agents Multimodel Execution")
def run_full_graph(pergunta: str):
    inputs = {"pergunta": pergunta}
    result = agent_graph.invoke(inputs)
    return result