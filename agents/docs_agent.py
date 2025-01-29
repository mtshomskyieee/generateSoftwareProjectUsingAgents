from crewai import Agent, Task

class DocsAgent:
    @staticmethod
    def create():
        return Agent(
            role='Technical Writer',
            goal='Create clear calculator application documentation',
            backstory="""You are a technical writer specialized in creating user-friendly
            documentation for command-line tools. You excel at explaining mathematical
            concepts and software usage clearly.""",
            tools=[],
            verbose=True
        )

    @staticmethod
    def create_task(agent, project_info, output_file=None):
        if output_file is None:
            output_file = 'docs/README.md'

        return Task(
            description=f"""Create comprehensive documentation for the calculator application:
            {project_info}

            Documentation should include:
            1. Installation and setup
            2. Available operations
            3. Usage examples
            4. Error handling guide
            5. History feature usage""",
            agent=agent,
            expected_output="""Complete calculator documentation including:
            - Clear installation instructions
            - Detailed operation guide
            - Example calculations
            - Troubleshooting section
            - History feature explanation""",
            output_file=output_file
        )