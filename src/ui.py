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

        # Step 1: Analyze the question to identify topics
        analyze_question_result = crew.agents[0].execute_task(
            crew.tasks[0],
            inputs={
                "user_message": prompt,
                "context": "\n".join(context)
            }
        )

        # Step 2: Find relevant information based on identified topics
        find_information_result = crew.agents[1].execute_task(
            crew.tasks[1],
            inputs={
                "user_message": prompt,
                "context": "\n".join(context),
                "identified_topics": analyze_question_result
            }
        )

        # Step 3: Write the final answer using the relevant information
        write_final_answer_result = crew.agents[2].execute_task(
            crew.tasks[2],
            inputs={
                "user_message": prompt,
                "context": "\n".join(context),
                "identified_topics": analyze_question_result,
                "relevant_information": find_information_result
            }
        )

    # Use the final result
    result = write_final_answer_result

    st.session_state.messages.append({"role": "assistant", "content": result})
    st.chat_message("assistant").write(result)
