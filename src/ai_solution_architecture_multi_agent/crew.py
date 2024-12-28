from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool

pdf_search_tool = PDFSearchTool(
  pdf='knowledge/21_Laws_of_AI_Solutions_Architecture.pdf',
  config=dict(
        llm=dict(
            provider="openai", 
            config=dict(
                model="gpt-4o-mini",
            ),
        ),
        embedder=dict(
            provider="openai",
            config=dict(
                model="text-embedding-3-small",
            ),
        ),
    )
)

@CrewBase
class AiSolutionArchitectureMultiAgent():
	"""AiSolutionArchitectureMultiAgent crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def ai_solution_architecture_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['ai_solution_architecture_researcher'],
			verbose=True,
			tools=[pdf_search_tool]
		)

	@agent
	def ai_solution_architecture_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['ai_solution_architecture_analyst'],
			verbose=True
		)

	@agent
	def ai_solution_architecture_engineer(self) -> Agent:
		return Agent(
			config=self.agents_config['ai_solution_architecture_engineer'],
			verbose=True
		)
	
	@agent
	def ai_solution_architecture_summarizer(self) -> Agent:
		return Agent(
			config=self.agents_config['ai_solution_architecture_summarizer'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)
	
	@task
	def analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['analysis_task'],
		)
	
	@task
	def engineering_task(self) -> Task:
		return Task(
			config=self.tasks_config['engineering_task'],
		)
	
	@task
	def summarization_task(self) -> Task:
		return Task(
			config=self.tasks_config['summarization_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the AiSolutionArchitectureMultiAgent crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
