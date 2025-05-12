import sys
package = __import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from setup import CrewaiConversationalChatbotCrew
import streamlit as st

st.set_page_config(page_title="💬 ISIKlub Chatbot", page_icon="🤖")
st.title("💬 Chatbot ISIKlub")

crew = CrewaiConversationalChatbotCrew().crew()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salut 👋 ! Pose-moi une question sur ISIKlub."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Écris ta question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("ISIKlub réfléchit... 🤔"):
        context = [
            f'{m["role"]}: {m["content"]}' for m in st.session_state.messages if m["role"] != "system"
        ]

        result = crew.kickoff(inputs={
            "user_message": prompt
        })

    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result.raw)
