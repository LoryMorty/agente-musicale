import streamlit as st
from agent import inizializza_agente
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

st.set_page_config(page_title="AI Music Mentor", page_icon="🎵")
st.title("🎵 Il tuo Orientatore Musicale AI")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar per il controllo (Slide 20: Persistenza lato client)
with st.sidebar:
    st.header("Impostazioni Mentore")
    if st.button("Nuova Sessione (Reset)"):
        st.session_state.messages = []
        st.rerun()
    st.info("Questo agente usa Llama 3.3 70B per un ragionamento profondo.")

# Definiamo la personalità (Cap. 6, Pag. 286: Ingegneria dei Prompt)
SYSTEM_PROMPT = """Sei un esperto orientatore musicale di alto livello. 
Il tuo compito è guidare l'utente alla scoperta della musica.
1. ELOQUENZA: Rispondi in modo colto, chiaro e appassionato. Non essere telegrafico.
2. SCOPERTA: Se l'utente è vago, fagli domande per capire cosa gli piace (strumenti, ritmi, atmosfere).
3. COERENZA: Quando consigli un artista, spiega PERCHÉ si adatta ai gusti dell'utente.
4. STRUMENTI: Usa 'cerca_concerti' solo quando l'utente mostra interesse per eventi dal vivo.
5. BUDGET: Se l'utente menziona un budget (es. 75€), verifica se i prezzi dei biglietti sono compatibili.
Rispondi sempre in italiano elegante."""

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt_user := st.chat_input("Parlami dei tuoi gusti musicali o chiedimi un consiglio..."):
    st.session_state.messages.append({"role": "user", "content": prompt_user})
    with st.chat_message("user"):
        st.markdown(prompt_user)

    with st.chat_message("assistant"):
        with st.spinner("Sto riflettendo sul tuo percorso musicale..."):
            try:
                agente = inizializza_agente()
                
                # MEMORIA OTTIMIZZATA (Pag. 303): Solo System Prompt + ultimi 5 messaggi
                # Questo evita l'errore 429 mantenendo la coerenza
                input_msgs = [SystemMessage(content=SYSTEM_PROMPT)]
                for m in st.session_state.messages[-5:]:
                    if m["role"] == "user":
                        input_msgs.append(HumanMessage(content=m["content"]))
                    else:
                        input_msgs.append(AIMessage(content=m["content"]))
                
                risposta = agente.invoke({"messages": input_msgs})
                output = risposta["messages"][-1].content
                
                st.markdown(output)
                st.session_state.messages.append({"role": "assistant", "content": output})
            except Exception as e:
                st.error(f"Corto circuito tecnico: {str(e)}")
