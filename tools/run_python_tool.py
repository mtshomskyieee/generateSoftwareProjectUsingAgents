import subprocess
import os
import sys
from crewai.tools import BaseTool
from typing import Optional, Annotated


class RunPythonGetOutput(BaseTool):
    name: str = "RunPythonGetOutput"
    description: str = "Runs a Python file and returns its output"

    def _run(self, file_path: str, is_test: bool = False) -> str:
        """
        Run a Python file and return its output.

        Args:
            file_path: Path to the Python file to run
            is_test: Whether this is a test file (uses pytest if True)

        Returns:
            The output of the Python script
        """
        try:
            if not os.path.exists(file_path):
                return f"Error: File '{file_path}' does not exist."

            # Get the absolute path to the directory containing the file
            file_dir = os.path.dirname(os.path.abspath(file_path))

            # Find the src directory that should be used as the project root
            if file_path.startswith('./src/'):
                project_root = './src'
            else:
                project_root = os.path.abspath(os.path.dirname(file_path))
                while os.path.basename(project_root) != 'src' and project_root != '/':
                    parent = os.path.dirname(project_root)
                    if parent == project_root:  # Reached the filesystem root
                        break
                    project_root = parent

            # Set PYTHONPATH environment to include the project root
            env = os.environ.copy()
            if 'PYTHONPATH' in env:
                env['PYTHONPATH'] = f"{os.path.abspath(project_root)}:{env['PYTHONPATH']}"
            else:
                env['PYTHONPATH'] = os.path.abspath(project_root)

            if is_test:
                # If running tests, use pytest with the project root in sys.path
                result = subprocess.run(
                    ["python", "-m", "pytest", file_path, "-v"],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    env=env
                )
            else:
                # Normal Python execution with the project root in sys.path
                result = subprocess.run(
                    ["python", file_path],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    env=env
                )

            output = result.stdout
            error = result.stderr
            exit_code = result.returncode

            if exit_code != 0:
                return f"Error (exit code {exit_code}) running {file_path}:\n{error}\n{output}"

            if error:
                return f"Warning while running {file_path}:\n{error}\n\nOutput:\n{output}"

            return f"Output from {file_path} (success):\n{output}"

        except subprocess.TimeoutExpired:
            return f"Error: Execution of '{file_path}' timed out."
        except Exception as e:
            return f"Error running {file_path}: {str(e)}"