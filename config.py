import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GEMINI_TOKEN = os.getenv("GEMINI_API_KEY")
TAVILY_TOKEN = os.getenv("TAVILY_API_KEY")

# Instanciação do modelo LLM da Google
llm_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro-exp-03-25",
    temperature=0,
    api_key=GEMINI_TOKEN
)
