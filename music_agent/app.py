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

# --- SIDEBAR (Slide 6 - Monitoraggio Stato) ---
with st.sidebar:
    st.title("👤 Profilo Dinamico")
    st.info("L'AI apprende dai tuoi gusti e dalle sue stesse proposte.")
    
    st.subheader("🎵 Generi Preferiti")
    st.write(", ".join(st.session_state.profilo.generi) if st.session_state.profilo.generi else "In attesa...")
    
    st.subheader("🎸 Artisti in Target")
    st.write(", ".join(st.session_state.profilo.artisti) if st.session_state.profilo.artisti else "In attesa...")
    
    st.subheader("💰 Budget Disponibile")
    if st.session_state.profilo.budget_max:
        st.success(f"{st.session_state.profilo.budget_max} €")
    else:
        st.warning("Budget non fornito")
    
    st.subheader("📍 Località")
    st.write(st.session_state.profilo.localita if st.session_state.profilo.localita else "Da definire")

    if st.button("Reset Sessione"):
        st.session_state.messages = []
        st.session_state.profilo = ProfiloUtente()
        st.rerun()

# --- LOGICA AGENTE (Slide 16 - Planning) ---
st.title("🎵 Mentore Musicale Strategico")

def pulisci_risposta(testo):
    return re.sub(r'<function.*?>.*?</function>', '', testo, flags=re.DOTALL).strip()

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt_user := st.chat_input("Scrivi qui (es. 'Consigliami qualcosa di Blues')"):
    st.session_state.messages.append({"role": "user", "content": prompt_user})
    with st.chat_message("user"):
        st.markdown(prompt_user)

    with st.chat_message("assistant"):
        with st.spinner("Il Mentore sta analizzando e verificando i costi..."):
            try:
                agente = inizializza_agente()
                profilo_json = st.session_state.profilo.json()
                
                # System Prompt con gestione vincoli (Pag. 281 e 286)
                sys_msg = f"""Sei un Mentore Musicale. 
                PROFILO UTENTE: {profilo_json}
                
                REGOLE RIGIDE:
                1. BUDGET: Se l'utente vuole un concerto e il 'budget_max' è Null, DEVI chiederlo prima di proporre eventi.
                2. VERIFICA PREZZI: Quando proponi un concerto, riporta SEMPRE il prezzo trovato. 
                3. VALIDAZIONE: Se il prezzo supera il 'budget_max', segnalalo chiaramente e proponi alternative più economiche.
                4. ELOQUENZA: Sii colto e spiega i legami tra generi.
                """
                
                input_msgs = [SystemMessage(content=sys_msg)]
                for m in st.session_state.messages[-5:]:
                    role = "user" if m["role"] == "user" else "assistant"
                    input_msgs.append(HumanMessage(content=m["content"]) if role == "user" else AIMessage(content=m["content"]))
                
                risposta = agente.invoke({"messages": input_msgs})
                output = pulisci_risposta(risposta["messages"][-1].content)

                st.markdown(output)
                st.session_state.messages.append({"role": "assistant", "content": output})
                
                # --- PASSO DI RIFLESSIONE (Slide 18) ---
                # Analizziamo l'ultimo scambio per aggiornare il profilo
                ultimo_scambio = f"UTENTE: {prompt_user}\nASSISTENTE: {output}"
                st.session_state.profilo = estrai_profilo(ultimo_scambio, st.session_state.profilo)
                
            except Exception as e:
                st.error(f"Errore tecnico: {str(e)}")
    
    st.rerun()
