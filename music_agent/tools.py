from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain.tools import tool

wrapper = DuckDuckGoSearchAPIWrapper(region="it-it", max_results=5)
search = DuckDuckGoSearchRun(api_wrapper=wrapper)

@tool
def cerca_concerti_con_prezzi(query: str):
    """Cerca concerti includendo esplicitamente PREZZI dei biglietti e date. 
    Usa query come 'prezzi biglietti concerto [artista]'."""
    return search.run(f"prezzi biglietti ufficiali date concerti 2025 2026 {query}")

@tool
def info_approfondite_artista(artista: str):
    """Cerca biografia e stile di un artista per orientamento musicale."""
    return search.run(f"stile musicale generi influenze {artista}")

tools = [cerca_concerti_con_prezzi, info_approfondite_artista]
