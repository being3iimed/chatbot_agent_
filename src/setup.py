import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys
API_KEY = os.getenv('API_KEY')
LLM_MODEL = os.getenv('LLM_MODEL')

@CrewBase
class CrewaiConversationalChatbotCrew:
    """CrewAI Conversational Chatbot for ISIKlub"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Init LLM
    _llm = LLM(
        model=LLM_MODEL,
        base_url="https://api.groq.com/openai/v1/",
        api_key=API_KEY,
        temperature=0.4
    )

    # AGENTS ----------------------
    @agent
    def isiklub_question_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['isiklub_question_analyst'],
            llm= self._llm,
            verbose=True,
        )

    @agent
    def isiklub_knowledge_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['isiklub_knowledge_specialist'],
            llm= self._llm,
            verbose=True,
        )

    agent
    def isiklub_answer_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['isiklub_answer_writer'],
            llm= self._llm,
            verbose=True,
        )

    # TASKS ----------------------

    @task
    def analyze_question(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_question'],
            agent=self.isiklub_question_analyst()
        )

    @task
    def find_information(self) -> Task:
        return Task(
            config=self.tasks_config['find_information'],
            agent=self.isiklub_knowledge_specialist()
        )

    @task
    def write_final_answer(self) -> Task:
        return Task(
            config=self.tasks_config['write_final_answer'],
            agent=self.isiklub_answer_writer()
        )

    # CREW -----------------------

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.isiklub_question_analyst(),
                self.isiklub_knowledge_specialist(),
                self.isiklub_answer_writer()
            ],
            tasks=[
                self.analyze_question(),
                self.find_information(),
                self.write_final_answer()
            ],
            process=Process.sequential,
            verbose=True,
        )
