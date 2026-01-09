import os
from langchain_groq import ChatGroq
from state import ProfiloUtente
from dotenv import load_dotenv

load_dotenv()

def estrai_profilo(scambio_recente: str, profilo_attuale: ProfiloUtente) -> ProfiloUtente:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    structured_llm = llm.with_structured_output(ProfiloUtente)
    
    prompt = f"""Analizza l'ultimo scambio tra l'utente e l'assistente per aggiornare il profilo.
    
    REGOLE:
    1. Se l'assistente consiglia un artista e l'utente esprime gradimento, aggiungilo agli 'artisti'.
    2. Se l'utente menziona un budget o una città, aggiorna 'budget_max' o 'localita'.
    3. Non cancellare informazioni vecchie a meno che non siano contraddette.
    
    Profilo Attuale: {profilo_attuale.json()}
    Ultimo Scambio:
    {scambio_recente}
    """
    
    try:
        return structured_llm.invoke(prompt)
    except:
        return profilo_attuale
