from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import Tool
import textstat
from textblob import TextBlob  
from config import TAVILY_TOKEN

# --- Tool 1: Pesquisa Online com Tavily ---
@tool
def online_lookup(prompt: str = "") -> str:
    """
    Execute a web search based on the provided user prompt.
    Returns summarized relevant information.
    Maximum of 4 curated results using Tavily API.
    """
    search_client = TavilySearchResults(max_results=4, api_key=TAVILY_TOKEN)
    results = search_client.invoke(prompt)
    return results

# --- Tool 2: Contador de Palavras Local ---
@tool
def contar_palavras(texto: str) -> str:
    """count number of words in text."""
    num_palavras = len(texto.split())
    return f"O texto tem {num_palavras} palavras."

# --- Tool 3: Legibilidade com Flesch Reading Ease ---
@tool
def legibilidade_flesch(texto: str) -> str:
    """Available legigibility of text with Flesch Reading Ease."""
    score = textstat.flesch_reading_ease(texto)
    return f"A pontuação de legibilidade (Flesch) do texto é: {score:.2f}."

# --- Tool 4: Análise de Sentimento Local ---
@tool
def analise_sentimento(texto: str) -> str:
    """Analyze the sentiment of the text and classify it as positive, negative or neutral."""
    blob = TextBlob(texto)
    polaridade = blob.sentiment.polarity  # -1 (negativo) a +1 (positivo)
    if polaridade > 0.1:
        sentimento = "Positivo"
    elif polaridade < -0.1:
        sentimento = "Negativo"
    else:
        sentimento = "Neutro"
    return f"A análise de sentimento indica: {sentimento} (polaridade: {polaridade:.2f})."

# --- Tool 5: Correção Gramatical Local ---
@tool
def correcao_gramatical(texto: str) -> str:
    """Grammatically corrects English text (basic version)."""
    blob = TextBlob(texto)
    texto_corrigido = str(blob.correct())
    return f"Texto corrigido:\n{texto_corrigido}"

# --- Lista de Ferramentas Disponíveis ---
available_tools_online = [online_lookup]
available_tools_local = [
    contar_palavras,
    legibilidade_flesch,
    analise_sentimento,
    correcao_gramatical
]