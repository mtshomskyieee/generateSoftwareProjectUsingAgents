# agents/fix_code_agent.py
from crewai import Agent, Task

class FixCodeAgent:
    @staticmethod
    def create():
        return Agent(
            role='Code Improvement Specialist',
            goal='Analyze code review feedback and implement necessary code changes',
            backstory="""You are an expert software engineer specializing in code refactoring 
            and improvement. You can take detailed review feedback or an error dump and you
            make fixes to the errors, and fixes according to the feedback.""",
            verbose=True
        )

    @staticmethod
    def create_task(agent, code, review_feedback, implementation_file=None):
        if implementation_file is None:
            implementation_file = 'src/app.py'

        return Task(
            description=f"""Analyze the following code and review feedback, then implement necessary improvements:

            Original Code:
            {code}

            Review Feedback:
            {review_feedback}

            Your task is to:
            1. Carefully read and understand the review feedback
            2. Identify specific areas needing improvement
            3. Modify the code to address each point in the feedback
            4. Ensure the core functionality remains intact
            5. Apply best practices and coding standards
            6. Include appropriate comments explaining significant changes
            7. Use type hints and follow Python best practices
            8. Improve error handling if suggested
            9. Enhance code readability and maintainability""",
            agent=agent,
            expected_output="""Fully refactored and improved code with:
            - All review feedback addressed
            - Maintained original functionality
            - Improved code quality
            - Added or enhanced documentation
            - Plain text output without markdown formatting""",
            output_file=implementation_file
        )