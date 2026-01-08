from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain.tools import tool

wrapper = DuckDuckGoSearchAPIWrapper(region="it-it", max_results=3)
search = DuckDuckGoSearchRun(api_wrapper=wrapper)

@tool
def cerca_concerti(artista_o_genere: str):
    """Cerca date, luoghi e prezzi dei concerti. Utile per dare consigli pratici su eventi live."""
    return search.run(f"concerti prezzi biglietti 2025 2026 {artista_o_genere}")

@tool
def info_approfondite_artista(artista: str):
    """Cerca biografia e discografia di un artista per fornire un orientamento più colto."""
    return search.run(f"biografia discografia stile musicale {artista}")

tools = [cerca_concerti, info_approfondite_artista]
