from crewai import Crew
from agents.idl_agent import IDLAgent
from agents.code_agent import CodeAgent
from agents.test_agent import TestAgent
from agents.docs_agent import DocsAgent
from agents.run_agent import RunAgent
from agents.review_agent import ReviewAgent
from agents.manifest_agent import ManifestAgent
from utils.project_validator import ProjectValidator
from utils.file_handler import FileHandler
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
        # New review agent
        self.review_agent = ReviewAgent.create()
        logger.info("Agents initialized successfully")

    def execute(self):
        """
        Executes the complete project generation workflow.
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
            run_script_file =  relative_project_directory + '/' + run_script_file


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
                code_task.output if hasattr(code_task, 'output') else "",
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

            # Create crew for remaining tasks
            crew = Crew(
                agents=[self.idl_agent, self.code_agent, self.test_agent, self.docs_agent, self.run_agent],
                tasks=[idl_task, code_task, test_task, docs_task, run_task],
                verbose=True
            )

            # Introduce a review loop (i.e. iterative review until approved or a maximum iteration count)
            max_review_iterations = 3
            review_iteration = 0
            review_approved = False

            while review_iteration < max_review_iterations and not review_approved:
                # Execute the workflow and get results
                logger.info("Executing crew tasks")
                results = crew.kickoff()
                generated_files = self._process_results(results)
                logger.info("Crew tasks completed")

                # Using the generated code—here we review the main implementation file.
                generated_code = generated_files.get(implementation_file, "")
                if not generated_code:
                    logger.warning("No generated code was found to review.")
                    generated_code = ""

                # Create and execute the review task
                review_task = ReviewAgent.create_task(self.review_agent, generated_code)
                review_crew = Crew(
                    agents=[self.review_agent],
                    tasks=[review_task],
                    verbose=True
                )
                review_result = review_crew.kickoff()
                review_output = review_result[0] if isinstance(review_result, list) else review_result
                logger.info(f"Review output:\n{review_output}")

                if "Approved" in review_output:
                    review_approved = True
                    logger.info("Code review approved the generated code.")
                else:
                    logger.info("Code review requested revisions. Re-running generation tasks with feedback...")
                    # (Optionally, you could incorporate the review feedback in subsequent iterations.)
                    review_iteration += 1

            if not review_approved:
                logger.warning("Maximum review iterations reached. Proceeding with the last generated files.")

            # Process and save generated files
            logger.info("Processing and saving generated files")
            generated_files = self._process_results(results)
            output_dir = self.file_handler.save_project_files(generated_files)

            logger.info(f"Project generation completed. Output directory: {output_dir}")
            return results

        except Exception as e:
            logger.error(f"Error in project generation: {str(e)}", exc_info=True)
            raise

    def _process_results(self, results):
        """
        Process the results from the crew execution into file contents.
        """
        try:
            generated_files = {}

            # Process IDL output
            if hasattr(results, 'idl_task') and results.idl_task:
                generated_files['src/specification.idl'] = results.idl_task
                logger.info("Processed IDL output")

            # Process code output
            if hasattr(results, 'code_task') and results.code_task:
                generated_files['src/app.py'] = results.code_task
                logger.info("Processed code output")

            # Process test output
            if hasattr(results, 'test_task') and results.test_task:
                generated_files['tests/test_app.py'] = results.test_task
                logger.info("Processed test output")

            # Process documentation output
            if hasattr(results, 'docs_task') and results.docs_task:
                generated_files['docs/README.md'] = results.docs_task
                logger.info("Processed documentation output")

            return generated_files

        except Exception as e:
            logger.error(f"Error processing results: {str(e)}", exc_info=True)
            raise

    def add_feature(self, feature_desc):
        """
        Handles the addition of new features to the existing project.
        """
        try:
            logger.info(f"Starting feature addition: {feature_desc}")

            # Create feature-specific tasks
            code_task = CodeAgent.create_task(
                self.code_agent,
                f"Add this feature to the existing implementation: {feature_desc}"
            )

            test_task = TestAgent.create_task(
                self.test_agent,
                f"""New Implementation: {code_task.output if hasattr(code_task, 'output') else ''}
                Feature Description: {feature_desc}
                Write tests for the new feature"""
            )

            run_task = RunAgent.create_task(
                self.run_agent,
                self.project_spec,
                idl_task.output if hasattr(idl_task, 'output') else ""
            )

            docs_task = DocsAgent.create_task(
                self.docs_agent,
                f"""Update documentation with:
                1. New Feature: {feature_desc}
                2. Implementation: {code_task.output if hasattr(code_task, 'output') else ''}
                3. Test Coverage: {test_task.output if hasattr(test_task, 'output') else ''}"""
            )

            # Create crew for feature addition
            crew = Crew(
                agents=[self.code_agent, self.test_agent, self.docs_agent, self.run_agent],
                tasks=[code_task, test_task, docs_task, run_task],
                verbose=True
            )

            # Execute and process results
            results = crew.kickoff()
            generated_files = self._process_results(results)
            output_dir = self.file_handler.save_project_files(generated_files)

            logger.info(f"Feature addition completed. Output directory: {output_dir}")
            return results

        except Exception as e:
            logger.error(f"Error in feature addition: {str(e)}", exc_info=True)
            raise