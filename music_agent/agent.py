import os
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools import tools
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """Sei un esperto orientatore musicale di alto livello.
REGOLE DI RISPOSTA:
1. ELOQUENZA: Rispondi in modo colto e appassionato.
2. NO TECNICISMI: Non mostrare mai all'utente i nomi delle funzioni o i tag <function>. 
3. SEPARAZIONE: Se decidi di usare uno strumento, fallo. Ma nella tua risposta finale verso l'utente deve esserci SOLO testo pulito ed elegante.
4. Rispondi sempre in italiano."""

def inizializza_agente():
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)
    return create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
