import os
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools import tools
from dotenv import load_dotenv

load_dotenv()

def inizializza_agente():
    # Usiamo il modello 70B per la massima qualità del linguaggio
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)
    return create_react_agent(llm, tools)
