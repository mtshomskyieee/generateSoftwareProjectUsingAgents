from crewai import Crew

from agents.fix_code_agent import FixCodeAgent
from agents.idl_agent import IDLAgent
from agents.code_agent import CodeAgent
from agents.test_agent import TestAgent
from agents.docs_agent import DocsAgent
from agents.run_agent import RunAgent
from agents.review_agent import ReviewAgent
from agents.manifest_agent import ManifestAgent
from utils.project_validator import ProjectValidator
from utils.file_handler import FileHandler
from agents.run_and_test_agent import RunAndTestAgent
from tools.run_python_tool import RunPythonGetOutput
import json
import logging
import sys
import os

## We're working locally, so we turn off telemetry to 'telemetry.crewai.com`
os.environ["OTEL_SDK_DISABLED"] = "true"


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('project_generation.log')
    ]
)

logger = logging.getLogger(__name__)

class ProjectWorkflow:
    def __init__(self, project_spec):
        self.project_spec = project_spec
        self.validator = ProjectValidator()
        self.file_handler = FileHandler()

        # Verify OPENAI_API_KEY is set
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        # Initialize agents
        logger.info("Initializing agents...")
        self.manifest_agent = ManifestAgent.create()
        self.idl_agent = IDLAgent.create()
        self.code_agent = CodeAgent.create()
        self.run_agent = RunAgent.create()
        self.test_agent = TestAgent.create()
        self.docs_agent = DocsAgent.create()
        self.fix_code_agent = FixCodeAgent.create()
        self.run_and_test_agent = RunAndTestAgent.create()
        # New review agent
        self.review_agent = ReviewAgent.create()
        logger.info("Agents initialized successfully")

    def execute_orig(self):
        """
        Executes the complete project generation workflow with enhanced testing and iteration.
        """
        try:
            logger.info("Starting project generation workflow")
            logger.info(f"Processing specification:\n{self.project_spec}")

            # Validate initial specification
            logger.info("Validating project specification")
            self.validator.validate_specification(self.project_spec)

            # Create tasks with proper dependencies
            logger.info("Creating agent tasks")

            # Create and execute manifest task first
            manifest_task = ManifestAgent.create_task(self.manifest_agent, self.project_spec)
            logger.info("Manifest task created")

            # Execute manifest task separately to get file paths
            manifest_crew = Crew(
                agents=[self.manifest_agent],
                tasks=[manifest_task],
                verbose=True
            )
            manifest_result = manifest_crew.kickoff()
            logger.info("Manifest task executed")

            # Parse manifest output with proper error handling
            try:
                manifest_output = manifest_result[0] if isinstance(manifest_result, list) else manifest_result
                print(f"---------------->manifest {manifest_output} <----------------")
                if not manifest_output:
                    raise ValueError("Manifest task returned no output")
                manifest_data = json.loads(str(manifest_output))
                logger.info(f"Manifest data: {manifest_data}")
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Error parsing manifest output: {str(e)}")
                manifest_data = {
                    "implementation_file": "src/app.py",
                    "test_file": "tests/test_app.py",
                    "docs_file": "docs/README.md",
                    "interface_file": "src/app.idl",
                    "run_script": "build_and_run.sh",
                }
                logger.info(f"Using default manifest data: {manifest_data}")

            # Extract file paths from manifest
            implementation_file = manifest_data.get('implementation_file', 'src/app.py')
            test_file = manifest_data.get('test_file', 'src/test_app.py')
            docs_file = manifest_data.get('docs_file', 'src/README.md')
            interface_file = manifest_data.get('interface_file', 'src/app.idl')
            run_script_file = manifest_data.get('run_script', 'build_and_run.sh')

            relative_project_directory = "./src"
            implementation_file = relative_project_directory + '/' + implementation_file
            test_file = relative_project_directory + '/' + test_file
            docs_file = relative_project_directory + '/' + docs_file
            interface_file = relative_project_directory + '/' + interface_file
            run_script_file = relative_project_directory + '/' + run_script_file

            logger.info(f"--------------------------------------------")
            logger.info(f"implementation_file file: {implementation_file}")
            logger.info(f"test_file file: {test_file}")
            logger.info(f"docs_file file: {docs_file}")
            logger.info(f"interface_file file: {interface_file}")
            logger.info(f"run_script_file file: {run_script_file}")

            # Create required directories
            os.makedirs(os.path.dirname(implementation_file), exist_ok=True)
            os.makedirs(os.path.dirname(test_file), exist_ok=True)
            os.makedirs(os.path.dirname(docs_file), exist_ok=True)
            os.makedirs(os.path.dirname(interface_file), exist_ok=True)
            os.makedirs(os.path.dirname(run_script_file), exist_ok=True)

            # IDL Task
            idl_task = IDLAgent.create_task(
                self.idl_agent,
                self.project_spec,
                output_file=interface_file
            )
            logger.info("IDL task created")

            # Code Task
            code_task = CodeAgent.create_task(
                self.code_agent,
                self.project_spec,
                idl_task.output if hasattr(idl_task, "output") else "",
                output_file=implementation_file
            )
            logger.info("Code task created")

            # Run Task
            run_task = RunAgent.create_task(
                self.run_agent,
                self.project_spec,
                idl_task.output if hasattr(idl_task, 'output') else "",
                output_file=run_script_file
            )
            logger.info("run task created")

            # Test Task
            test_task = TestAgent.create_task(
                self.test_agent,
                code_file=implementation_file,
                code=code_task.output if hasattr(code_task, 'output') else "",
                output_file=test_file
            )
            logger.info("Test task created")

            # Documentation Task
            docs_task = DocsAgent.create_task(
                self.docs_agent,
                f"""Project Documentation:
                           Specification: {self.project_spec}
                           Implementation: {code_task.output if hasattr(code_task, 'output') else ""}
                           Testing: {test_task.output if hasattr(test_task, 'output') else ""}""",
                output_file=docs_file
            )
            logger.info("Documentation task created")

            max_iterations = 1
            iteration = 0
            final_generated_files = {}

            while iteration < max_iterations:
                iteration += 1
                logger.info(f"Project Generation Iteration {iteration}")

                # Create and execute crew tasks
                crew = Crew(
                    agents=[self.idl_agent, self.code_agent, self.test_agent, self.docs_agent, self.run_agent],
                    tasks=[idl_task, code_task, test_task, docs_task, run_task],
                    verbose=True
                )

                # After getting the crew results
                results = crew.kickoff()
                logger.info(f"results = {results}")
                #debug: user_input = input("Enter something: ")  # Prompts user and stores input in variable

                # Initial processing
                generated_files = self._process_results(results)

                # Store the code output immediately
                if implementation_file not in generated_files:
                    # Get the code from the results directly if possible
                    code_output = next((r for r in results if isinstance(r, str) and 'def' in r), None)
                    if code_output:
                        generated_files[implementation_file] = code_output
                        logger.info(f"Stored generated code in {implementation_file}")

                ## Implement Reviews ##
                # Introduce a review loop (i.e. iterative review until approved or a maximum iteration count)
                max_review_iterations = 2
                review_iteration = 0
                review_approved = False

                while review_iteration < max_review_iterations and not review_approved:
                    # Execute the workflow and get results
                    logger.info("Executing crew tasks")
                    results = crew.kickoff()
                    generated_files = self._process_results(results)
                    logger.info("Crew tasks completed")

                    # Before reviewing the code, add better error handling
                    generated_code = generated_files.get(implementation_file)
                    if not generated_code:
                        logger.error(f"Failed to find generated code at path: {implementation_file}")
                        logger.error(f"Available files: {list(generated_files.keys())}")
                        generated_code = "" # Provide empty string as fallback

                    # Create and execute the review task
                    review_task = ReviewAgent.create_task(self.review_agent, generated_code)
                    review_crew = Crew(
                        agents=[self.review_agent],
                        tasks=[review_task],
                        verbose=True
                    )
                    review_result = review_crew.kickoff()
                    review_output = self._extract_content(review_result)
                    logger.info(f"Review output:\n{review_output}")

                    if "Approved" in review_output:
                        review_approved = True
                        logger.info("Code review approved the generated code.")
                    else:
                        # If review suggests revisions, use the FixCodeAgent
                        logger.info("Code review requested revisions. Fixing code...")

                        # Before calling fix_code_agent
                        logger.info(f"Code state before fix: {len(generated_code) if generated_code else 'empty'}")
                        fix_code_task = FixCodeAgent.create_task(
                            self.fix_code_agent,
                            generated_code,  # The current code
                            review_output,  # Review feedback
                            implementation_file  # Where to save the fixed code
                        )

                        fix_code_crew = Crew(
                            agents=[self.fix_code_agent],
                            tasks=[fix_code_task],
                            verbose=True
                        )

                        fix_results = fix_code_crew.kickoff()
                        # Later when processing fixes
                        generated_files = self._process_results(fix_results, generated_files)

                        review_iteration += 1

                if not review_approved:
                    logger.warning(f"Maximum review iterations reached({review_iteration}). Proceeding with the last generated files.")

                # Run tests with the RunAndTestAgent
                if implementation_file.endswith('.py'):
                    logger.info("Running execution and testing")
                    run_and_test_task = RunAndTestAgent.create_task(
                        self.run_and_test_agent,
                        implementation_file,
                        test_file,
                        output_file=os.path.join(os.path.dirname(implementation_file), "execution_result.txt")
                    )

                    run_test_crew = Crew(
                        agents=[self.run_and_test_agent],
                        tasks=[run_and_test_task],
                        verbose=True
                    )
                    run_test_result = run_test_crew.kickoff()

                    # Analyze test results
                    test_output = self._extract_content(run_test_result)

                    # Check if tests passed
                    if "ALL TESTS PASSED" in test_output:
                        logger.info("Tests passed successfully!")
                        break
                    else:
                        logger.info(f"Tests failed on iteration {iteration}. Regenerating...")

                        # Analyze failure and update tasks

                        fix_code_task = FixCodeAgent.create_task(
                            self.fix_code_agent,
                            generated_code,  # The current code
                            test_output,  # Review feedback
                            implementation_file  # Where to save the fixed code
                        )

                        fix_code_crew = Crew(
                            agents=[self.fix_code_agent],
                            tasks=[fix_code_task],
                            verbose=True
                        )

                        fix_results = fix_code_crew.kickoff()

                        # Update the generated code with the fixed version
                        generated_code = self._extract_content(fix_results)
                        generated_files[implementation_file] = generated_code


            # Final check
            if iteration >= max_iterations:
                logger.warning("Maximum iterations reached without successful test pass")

            final_generated_files = generated_files

            # Process and save generated files
            output_dir = self.file_handler.save_project_files(final_generated_files)
            logger.info(f"Project generation completed. Output directory: {output_dir}")

            return final_generated_files

        except Exception as e:
            logger.error(f"Error in project generation: {str(e)}", exc_info=True)
            raise

    def execute(self):
        """
        Executes the complete project generation workflow with enhanced testing and iteration.
        """
        try:
            logger.info("Starting project generation workflow")
            logger.info(f"Processing specification:\n{self.project_spec}")

            # Validate initial specification
            logger.info("Validating project specification")
            self.validator.validate_specification(self.project_spec)

            # Create tasks with proper dependencies
            logger.info("Creating agent tasks")

            # Create and execute manifest task first
            manifest_task = ManifestAgent.create_task(self.manifest_agent, self.project_spec)
            logger.info("Manifest task created")

            # Execute manifest task separately to get file paths
            manifest_crew = Crew(
                agents=[self.manifest_agent],
                tasks=[manifest_task],
                verbose=True
            )
            manifest_result = manifest_crew.kickoff()
            logger.info("Manifest task executed")

            # Parse manifest output with proper error handling
            try:
                manifest_output = manifest_result[0] if isinstance(manifest_result, list) else manifest_result
                print(f"---------------->manifest {manifest_output} <----------------")
                if not manifest_output:
                    raise ValueError("Manifest task returned no output")
                manifest_data = json.loads(str(manifest_output))
                logger.info(f"Manifest data: {manifest_data}")
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Error parsing manifest output: {str(e)}")
                manifest_data = {
                    "implementation_file": "src/app.py",
                    "test_file": "tests/test_app.py",
                    "docs_file": "docs/README.md",
                    "interface_file": "src/app.idl",
                    "run_script": "build_and_run.sh",
                }
                logger.info(f"Using default manifest data: {manifest_data}")

            # Extract file paths from manifest
            implementation_file = manifest_data.get('implementation_file', 'src/app.py')
            test_file = manifest_data.get('test_file', 'src/test_app.py')
            docs_file = manifest_data.get('docs_file', 'src/README.md')
            interface_file = manifest_data.get('interface_file', 'src/app.idl')
            run_script_file = manifest_data.get('run_script', 'build_and_run.sh')

            relative_project_directory = "./src"
            implementation_file = relative_project_directory + '/' + implementation_file
            test_file = relative_project_directory + '/' + test_file
            docs_file = relative_project_directory + '/' + docs_file
            interface_file = relative_project_directory + '/' + interface_file
            run_script_file = relative_project_directory + '/' + run_script_file

            # Store file paths for use throughout the workflow
            file_paths = {
                'implementation_file': implementation_file,
                'test_file': test_file,
                'docs_file': docs_file,
                'interface_file': interface_file,
                'run_script': run_script_file
            }

            logger.info(f"--------------------------------------------")
            logger.info(f"implementation_file file: {implementation_file}")
            logger.info(f"test_file file: {test_file}")
            logger.info(f"docs_file file: {docs_file}")
            logger.info(f"interface_file file: {interface_file}")
            logger.info(f"run_script_file file: {run_script_file}")

            # Create required directories
            os.makedirs(os.path.dirname(implementation_file), exist_ok=True)
            os.makedirs(os.path.dirname(test_file), exist_ok=True)
            os.makedirs(os.path.dirname(docs_file), exist_ok=True)
            os.makedirs(os.path.dirname(interface_file), exist_ok=True)
            os.makedirs(os.path.dirname(run_script_file), exist_ok=True)

            max_iterations = 1
            iteration = 0
            final_generated_files = {}
            current_generated_code = ""  # Track the current generated code

            while iteration < max_iterations:
                iteration += 1
                logger.info(f"Project Generation Iteration {iteration}")

                # IDL Task
                idl_task = IDLAgent.create_task(
                    self.idl_agent,
                    self.project_spec,
                    output_file=interface_file
                )
                logger.info("IDL task created")

                # Execute IDL task first to get the IDL output
                idl_crew = Crew(
                    agents=[self.idl_agent],
                    tasks=[idl_task],
                    verbose=True
                )
                idl_result = idl_crew.kickoff()
                idl_output = self._extract_content(idl_result)

                # Code Task
                code_task = CodeAgent.create_task(
                    self.code_agent,
                    self.project_spec,
                    str(idl_output),
                    output_file=implementation_file
                )
                logger.info("Code task created")

                code_crew = Crew(
                    agents=[self.code_agent],
                    tasks=[code_task],
                    verbose=True
                )
                code_result = code_crew.kickoff()
                current_generated_code = self._extract_content(code_result)
                logger.info(f"Generated code length: {len(current_generated_code) if current_generated_code else 0}")

                test_task = TestAgent.create_task(
                    self.test_agent,
                    code_file=implementation_file,
                    code=current_generated_code,
                    output_file=test_file
                )
                logger.info("Test task created")

                # Execute test task
                test_crew = Crew(
                    agents=[self.test_agent],
                    tasks=[test_task],
                    verbose=True
                )
                test_result = test_crew.kickoff()
                test_output = self._extract_content(test_result)

                # Run Task
                run_task = RunAgent.create_task(
                    self.run_agent,
                    self.project_spec,
                    str(idl_output),
                    output_file=run_script_file
                )
                logger.info("run task created")

                # Execute run task
                run_crew = Crew(
                    agents=[self.run_agent],
                    tasks=[run_task],
                    verbose=True
                )
                run_result = run_crew.kickoff()
                run_output = self._extract_content(run_result)

                # Documentation Task
                docs_task = DocsAgent.create_task(
                    self.docs_agent,
                    f"""Project Documentation:
                               Specification: {self.project_spec}
                               Implementation: {current_generated_code}
                               Testing: {test_output}""",
                    output_file=docs_file
                )
                logger.info("Documentation task created")

                # Execute docs task
                docs_crew = Crew(
                    agents=[self.docs_agent],
                    tasks=[docs_task],
                    verbose=True
                )
                docs_result = docs_crew.kickoff()
                docs_output = self._extract_content(docs_result)
                # Combine all results
                all_results = [idl_output, current_generated_code, test_output, docs_output, run_output]

                # Process results with the correct file paths
                generated_files = self._process_results(all_results, existing_files=None, file_paths=file_paths)

                ## Implement Reviews ##
                max_review_iterations = 2
                review_iteration = 0
                review_approved = False

                while review_iteration < max_review_iterations and not review_approved:
                    review_iteration += 1
                    logger.info(f"Review iteration {review_iteration}")

                    # Before reviewing the code, ensure we have the current code
                    if not current_generated_code:
                        logger.error("No generated code available for review")
                        break

                    # Create and execute the review task
                    review_task = ReviewAgent.create_task(self.review_agent, current_generated_code)
                    review_crew = Crew(
                        agents=[self.review_agent],
                        tasks=[review_task],
                        verbose=True
                    )
                    review_result = review_crew.kickoff()
                    review_output = self._extract_content(review_result)
                    logger.info(f"Review output:\n{review_output}")

                    if "Approved" in review_output:
                        review_approved = True
                        logger.info("Code review approved the generated code.")
                    else:
                        # If review suggests revisions, use the FixCodeAgent
                        logger.info("Code review requested revisions. Fixing code...")
                        logger.info(
                            f"Code state before fix: {len(current_generated_code) if current_generated_code else 'empty'}")

                        fix_code_task = FixCodeAgent.create_task(
                            self.fix_code_agent,
                            current_generated_code,  # Pass the current code
                            review_output,  # Review feedback
                            implementation_file  # Where to save the fixed code
                        )

                        fix_code_crew = Crew(
                            agents=[self.fix_code_agent],
                            tasks=[fix_code_task],
                            verbose=True
                        )

                        fix_results = fix_code_crew.kickoff()
                        # Update the current generated code with the fixed version
                        current_generated_code =  self._extract_content(fix_results)

                        # Update the generated files with the fixed code
                        generated_files[implementation_file] = current_generated_code
                        logger.info(
                            f"Code fixed, new length: {len(current_generated_code) if current_generated_code else 'empty'}")

                if not review_approved:
                    logger.warning("Maximum review iterations reached. Proceeding with the last generated files.")

                # Run tests with the RunAndTestAgent
                if implementation_file.endswith('.py'):
                    logger.info("Running execution and testing")
                    run_and_test_task = RunAndTestAgent.create_task(
                        self.run_and_test_agent,
                        implementation_file,
                        test_file,
                        output_file=os.path.join(os.path.dirname(implementation_file), "execution_result.txt")
                    )

                    run_test_crew = Crew(
                        agents=[self.run_and_test_agent],
                        tasks=[run_and_test_task],
                        verbose=True
                    )
                    run_test_result = run_test_crew.kickoff()

                    # Analyze test results
                    test_output = self._extract_content(run_test_result)

                    # Check if tests passed
                    if "ALL TESTS PASSED" in test_output:
                        logger.info("Tests passed successfully!")
                        final_generated_files = generated_files
                        break
                    else:
                        logger.info(f"Tests failed on iteration {iteration}. Regenerating...")

                        # Use FixCodeAgent to fix test failures
                        fix_code_task = FixCodeAgent.create_task(
                            self.fix_code_agent,
                            current_generated_code,  # The current code
                            test_output,  # Test failure feedback
                            implementation_file  # Where to save the fixed code
                        )

                        fix_code_crew = Crew(
                            agents=[self.fix_code_agent],
                            tasks=[fix_code_task],
                            verbose=True
                        )

                        fix_results = fix_code_crew.kickoff()

                        # Update the current generated code with the fixed version
                        current_generated_code = self._extract_content(fix_results)
                        generated_files[implementation_file] = current_generated_code

                final_generated_files = generated_files

            # Final check
            if iteration >= max_iterations:
                logger.warning("Maximum iterations reached without successful test pass")
                final_generated_files = generated_files

            # Process and save generated files
            output_dir = self.file_handler.save_project_files(final_generated_files)
            logger.info(f"Project generation completed. Output directory: {output_dir}")

            return final_generated_files

        except Exception as e:
            logger.error(f"Error in project generation: {str(e)}", exc_info=True)
            raise

    def _process_results(self, results, existing_files=None, file_paths=None):
        """
        Process the results from the crew execution into file contents.
        """
        try:
            generated_files = existing_files if existing_files is not None else {}

            # Use provided file_paths or fall back to defaults
            if file_paths is None:
                file_paths = {
                    'implementation_file': './src/app.py',
                    'test_file': './src/test_app.py',
                    'docs_file': './src/README.md',
                    'interface_file': './src/app.idl',
                    'run_script': './src/build_and_run.sh'
                }

            # Extract content from results using the utility function
            if isinstance(results, list) and len(results) >= 5:
                idl_output = self._extract_content(results[0])
                code_output = self._extract_content(results[1])
                test_output = self._extract_content(results[2])
                docs_output = self._extract_content(results[3])
                run_output = self._extract_content(results[4])
            elif isinstance(results, list) and len(results) > 0:
                code_output = self._extract_content(results[0])
                idl_output = test_output = docs_output = run_output = None
            else:
                code_output = self._extract_content(results)
                idl_output = test_output = docs_output = run_output = None

            # Use the actual file paths from manifest
            if code_output:
                generated_files[file_paths['implementation_file']] = code_output
                logger.info(f"Processed code output to {file_paths['implementation_file']}")

            if test_output:
                generated_files[file_paths['test_file']] = test_output
                logger.info(f"Processed test output to {file_paths['test_file']}")

            if docs_output:
                generated_files[file_paths['docs_file']] = docs_output
                logger.info(f"Processed documentation output to {file_paths['docs_file']}")

            if idl_output:
                generated_files[file_paths['interface_file']] = idl_output
                logger.info(f"Processed IDL output to {file_paths['interface_file']}")

            if run_output:
                generated_files[file_paths['run_script']] = run_output
                logger.info(f"Processed run script to {file_paths['run_script']}")

            # Always add initialization files
            generated_files['./src/src/__init__.py'] = '# Python package initialization'
            generated_files['./src/tests/__init__.py'] = '# Python tests package initialization'

            return generated_files

        except Exception as e:
            logger.error(f"Error processing results: {str(e)}", exc_info=True)
            raise

    def _extract_content(self, crew_output):
        """
        Extract the actual content from CrewOutput objects or other result types.
        """
        if crew_output is None:
            return ""

        # Handle list of results
        if isinstance(crew_output, list):
            if len(crew_output) > 0:
                crew_output = crew_output[0]
            else:
                return ""

        # Handle CrewOutput objects
        if hasattr(crew_output, 'raw_output'):
            return str(crew_output.raw_output)
        elif hasattr(crew_output, 'output'):
            return str(crew_output.output)
        elif hasattr(crew_output, 'result'):
            return str(crew_output.result)
        else:
            return str(crew_output)