from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import llm_model
from agents.personas import persona_message_2, persona_message_4

# Prompt para o Agente 2
post_prompt = ChatPromptTemplate.from_messages([
    persona_message_2,
    ("human", "Here is the research summary: {research_summary}\n\nWrite a social media post based on this.")
])
agent_2_chain = post_prompt | llm_model | StrOutputParser()

# Prompt para o Agente 4
final_review_prompt = ChatPromptTemplate.from_messages([
    persona_message_4,
    ("human", 
     "Here is the original research:\n\n{pesquisa_inicial}\n\n"
     "Here is the enhanced post:\n\n{post_incrementado}\n\n"
     "Write the final reviewed post.")
])
agent_4_chain = final_review_prompt | llm_model | StrOutputParser()
