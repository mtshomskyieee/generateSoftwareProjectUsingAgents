from crewai import Agent, Task
from tools.run_python_tool import RunPythonGetOutput
import re
import os
from datetime import datetime


class RunAndTestAgent:
    @staticmethod
    def create():
        return Agent(
            role='Testing and Execution Specialist',
            goal='Execute Python code and verify it works as expected through testing',
            backstory="""You are a specialist in running and testing Python code. You can 
            execute Python files, run their associated tests, and determine if they're 
            functioning correctly. You're persistent and will retry up to 5 times   
            if the code or tests fail, making necessary improvements each time.""",
            tools=[RunPythonGetOutput()],
            verbose=True
        )

    @staticmethod
    def create_task(agent, code_file, test_file, output_file=None):
        if output_file is None:
            output_file = 'src/execution_result.txt'

        return Task(
            description=f"""Execute the Python file at {code_file} and run its tests at {test_file} to verify it works properly.

            Your job is to:
            1. Run the Python file using the RunPythonGetOutput tool
            2. Run the test file using the RunPythonGetOutput tool with is_test=True
            3. Analyze both outputs to ensure the code works correctly and passes all tests
            4. If there are errors or test failures, analyze the issues and suggest fixes
            5. Some tests with input_invalid are expected to throw errors or fail, analyze these errors separately
            6. You should retry up to 3 times if tests fail, implementing your suggested fixes
            7. Track all test failures and append them to testing_agent_output.txt

            The code should execute without errors and ALL tests should pass.
            """,
            agent=agent,
            expected_output="""A detailed report of the execution and testing results including:
            - The output from running the Python file
            - The results of running the tests
            - Analysis of any failures and how they were resolved
            - Number of retries needed
            - Final status (Success/Failure)
            """,
            output_file=output_file
        )

    @staticmethod
    def log_test_failure(code_file, test_file, test_output, attempt_number, suggestions=None):
        """
        Log test failures to the testing_agent_output.txt file
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract failure information
        failure_lines = []
        for line in test_output.split('\n'):
            if 'FAIL' in line or 'ERROR' in line or 'failed' in line.lower() or 'error' in line.lower():
                failure_lines.append(line)

        failure_summary = '\n'.join(
            failure_lines) if failure_lines else "Tests failed but no specific failure message found"

        # Create the log entry
        log_entry = f"""
=================================================
TIMESTAMP: {timestamp}
CODE FILE: {code_file}
TEST FILE: {test_file}
ATTEMPT: {attempt_number}
FAILURES:
{failure_summary}
"""

        if suggestions:
            log_entry += f"""
SUGGESTIONS:
{suggestions}
"""

        log_entry += "=================================================\n"

        # Append to the log file
        with open('testing_agent_output.txt', 'a') as f:
            f.write(log_entry)

    @staticmethod
    def execute_with_retries(agent, code_file, test_file, max_retries=3):
        """
        Execute code and tests with retries if tests fail.
        Logs failures to testing_agent_output.txt
        """
        retries = 0
        success = False
        results = []

        while retries < max_retries and not success:
            attempt_number = retries + 1
            # Run the code
            code_output = agent.tools[0]._run(code_file)
            results.append(f"Run attempt {attempt_number}:\n{code_output}\n")

            # Run the tests
            test_output = agent.tools[0]._run(test_file, is_test=True)
            results.append(f"Test attempt {attempt_number}:\n{test_output}\n")

            # Check for test success
            if "failed" not in test_output.lower() and "error" not in test_output.lower():
                success = True
                results.append("ALL TESTS PASSED! 🎉")

                # Log successful run after previous failures
                if retries > 0:
                    with open('testing_agent_output.txt', 'a') as f:
                        f.write(f"\nTIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"SUCCESS after {attempt_number} attempts for {code_file} with {test_file}\n\n")
                break

            # If tests failed, analyze and suggest fixes
            # Generate suggestions (in real implementation, the agent's intelligence would do this)
            suggestions = f"Identified issues in test attempt {attempt_number}. Recommend reviewing error messages and fixing the code."
            results.append(f"Tests failed on attempt {attempt_number}. Analyzing issues...")
            results.append(suggestions)

            # Log the failure
            RunAndTestAgent.log_test_failure(code_file, test_file, test_output, attempt_number, suggestions)

            retries += 1

        if not success:
            final_message = f"Failed after {max_retries} attempts. Please review the code and tests manually."
            results.append(final_message)

            # Log final failure
            with open('testing_agent_output.txt', 'a') as f:
                f.write(f"\nTIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"FINAL FAILURE: {final_message} for {code_file} with {test_file}\n\n")

        return "\n".join(results)