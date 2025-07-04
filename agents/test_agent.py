from crewai import Agent, Task

class TestAgent:
    @staticmethod
    def create():
        return Agent(
            role='Testing Specialist',
            goal='Create comprehensive tests for the generated code',
            backstory="""You are a QA engineer specialized in creating thorough test 
            suites. You ensure code reliability through comprehensive test coverage 
            and edge case handling for any programming language.""",
            tools=[],
            verbose=True
        )

    @staticmethod
    def create_task(agent, code_file, code, output_file):
        return Task(
            description=f"""Create comprehensive unit tests in the target language for the generated code saved at
            {code_file} here is the code:
            {code}

            Test suite must cover:
            0. Include whatever is necessary from the code file at  {code_file}
            1. Be written in the same language as the code
            2. All public interfaces and methods
            3. Include pathing if needed; for example for libraries in a directory named src that are being tested import like so, Python=import src.<packagename>, c/C++=include "src/<packagename>, etc.
            4. Error handling scenarios
            5. Edge cases and boundary conditions
            6. Integration tests where applicable
            7. Input validation""",
            agent=agent,
            expected_output="""Complete test suite in the specified language including:
            - Unit tests for all public methods
            - Error handling verification
            - Edge case coverage
            - Integration tests
            - Documentation of test scenarios
            - The file is plain text, it isn't markdown
            - Plain Text, remove Markdown""",
            output_file=output_file
        )