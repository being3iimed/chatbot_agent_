# Documentation
### Overview

This project is a chatbot system built with **FastAPI** for the backend and **Streamlit** for the user interface. It uses the **CrewAI** framework to define agents, tasks, and workflows for processing user queries. The chatbot analyzes questions, retrieves relevant information, and generates structured responses.

### Key Features

1. **Backend API**:
   - FastAPI server with a `/chat` endpoint to process user messages.
   - Uses `CrewaiConversationalChatbotCrew` to manage agents and tasks.

2. **Streamlit UI**:
   - Web-based interface for user interaction.
   - Tracks conversation history and displays responses.

3. **CrewAI Workflow**:
   - Agents:
     - `isiklub_question_analyst`: Analyzes user questions.
     - `isiklub_knowledge_specialist`: Retrieves relevant information.
     - `isiklub_answer_writer`: Generates user-friendly responses.
   - Tasks:
     - `analyze_question`, `find_information`, `write_final_answer`.

4. **Configuration**:
   - `.env` file for sensitive data like `GROQ_API_KEY` and `LLM_MODEL`.
   - YAML files (`agents.yaml`, `tasks.yaml`) to define agents and tasks.

5. **Dependencies**:
   - Includes `streamlit`, `crewai`, `fastapi`, and others.

### How It Works

1. **User Interaction**:
   - Users interact via Streamlit or FastAPI.
   - Input is processed by the CrewAI workflow.

2. **Processing Workflow**:
   - Questions are analyzed, information is retrieved, and responses are generated.

3. **Response Delivery**:
   - Responses are displayed in the Streamlit UI or returned via the API.

### Purpose

The chatbot assists users by answering questions about services, providing accurate and structured responses to enhance the user experience.