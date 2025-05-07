import os
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from groq import Groq

# Init LLM
llm = Groq(
    model="llama-3.1-70b-versatile",
    api_key=os.environ["GROQ_API_KEY"],
)

@CrewBase
class CrewaiConversationalChatbotCrew:
    """CrewAI Conversational Chatbot for ISIKlub"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # AGENTS ----------------------

    @agent
    def isiklub_question_analyst(self) -> Agent:
        return Agent(
            config="isiklub_question_analyst",
            llm= LLM(
                model="groq/gemma2-9b-it",
                temperature=0.7
            ),
            verbose=True,
        )

    @agent
    def isiklub_knowledge_specialist(self) -> Agent:
        return Agent(
            config="isiklub_knowledge_specialist",
            llm=llm,
            verbose=True,
        )

    @agent
    def isiklub_answer_writer(self) -> Agent:
        return Agent(
            config="isiklub_answer_writer",
            llm=llm,
            verbose=True,
        )

    # TASKS ----------------------

    @task
    def analyze_question(self) -> Task:
        return Task(
            config="analyze_question",
            agent=self.isiklub_question_analyst()
        )

    @task
    def find_information(self) -> Task:
        return Task(
            config="find_information",
            agent=self.isiklub_knowledge_specialist()
        )

    @task
    def write_final_answer(self) -> Task:
        return Task(
            config="write_final_answer",
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
