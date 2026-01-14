import streamlit as st
import re
from agent import inizializza_agente
from parser import estrai_profilo
from state import ProfiloUtente
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

st.set_page_config(page_title="AI Music Mentor Pro", page_icon="🎵", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "profilo" not in st.session_state:
    st.session_state.profilo = ProfiloUtente()

with st.sidebar:
    st.title("👤 Profilo Dinamico")
    st.subheader("🎵 Generi")
    st.write(", ".join(st.session_state.profilo.generi) if st.session_state.profilo.generi else "In attesa...")
    st.subheader("🎸 Artisti")
    st.write(", ".join(st.session_state.profilo.artisti) if st.session_state.profilo.artisti else "In attesa...")
    st.subheader("💰 Budget")
    st.write(f"{st.session_state.profilo.budget_max} €" if st.session_state.profilo.budget_max else "Non specificato")
    if st.button("Reset Sessione"):
        st.session_state.messages = []
        st.session_state.profilo = ProfiloUtente()
        st.rerun()

st.title("🎵 Mentore Musicale Strategico")

def pulisci_risposta(testo):
    return re.sub(r'<function.*?>.*?</function>', '', testo, flags=re.DOTALL).strip()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt_user := st.chat_input("Parlami della tua musica preferita..."):
    st.session_state.messages.append({"role": "user", "content": prompt_user})
    with st.chat_message("user"):
        st.markdown(prompt_user)

    with st.chat_message("assistant"):
        with st.spinner("Il Mentore sta tracciando un percorso per te..."):
            try:
                agente = inizializza_agente()
                
                # Inseriamo il profilo reale dell'utente nel prompt di sistema (Slide 10)
                from agent import SYSTEM_PROMPT
                current_sys_prompt = SYSTEM_PROMPT.replace("{{profilo_json}}", st.session_state.profilo.json())
                
                input_msgs = [SystemMessage(content=current_sys_prompt)]
                # Inviamo la cronologia recente
                for m in st.session_state.messages[-5:]:
                    role = "user" if m["role"] == "user" else "assistant"
                    input_msgs.append(HumanMessage(content=m["content"]) if role == "user" else AIMessage(content=m["content"]))
                
                risposta = agente.invoke({"messages": input_msgs})
                output = pulisci_risposta(risposta["messages"][-1].content)

                st.markdown(output)
                st.session_state.messages.append({"role": "assistant", "content": output})
                
                # Riflessione per aggiornare il profilo (Slide 18)
                ultimo_scambio = f"UTENTE: {prompt_user}\nASSISTENTE: {output}"
                st.session_state.profilo = estrai_profilo(ultimo_scambio, st.session_state.profilo)
                
            except Exception as e:
                st.error(f"Errore tecnico: {str(e)}")
    
    st.rerun()
