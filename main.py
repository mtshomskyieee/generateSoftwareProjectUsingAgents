from crewai import Crew
from utils.file_handler import FileHandler
from workflows.project_workflow import ProjectWorkflow
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Project Generator using CrewAI')
    parser.add_argument('spec_file', help='Path to the project specification file')
    args = parser.parse_args()

    try:
        # Initialize file handler and read specification
        file_handler = FileHandler()
        project_spec = file_handler.read_specification(args.spec_file)

        # Initialize and run the project workflow
        workflow = ProjectWorkflow(project_spec)
        result = workflow.execute()

        print("\nProject generation completed successfully!")
        
        # Feature addition loop
        while True:
            add_feature = input("\nWould you like to add more features? (yes/no): ").lower()
            if add_feature != 'yes':
                break
                
            feature_desc = input("Please describe the new feature: ")
            workflow.add_feature(feature_desc)

    except FileNotFoundError:
        print(f"Error: Specification file '{args.spec_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
