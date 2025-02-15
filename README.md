# How to Run the Project Generator

## Writups and demo about this here
- https://medium.com/@mtshomsky/crewai-using-agents-to-code-1ad90190be21
- https://medium.com/@mtshomsky/crewai-using-agents-to-code-part2-d20ffc747b46

## Prerequisites
1. Python 3.6 or higher
2. Required packages (will be installed automatically):
   - crewai
   - langchain
   - openai
   - python-dotenv

## Setup

1. Install the required and optional dependencies:
```bash
pip install crewai langchain openai python-dotenv
```

2. Set up your OpenAI API key:
   - Create a `.env` file in the root directory
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

## Project Structure
```

├── agents/                 # AI agents for different tasks
│   ├── code_agent.py      # Generates implementation code
│   ├── docs_agent.py      # Creates documentation
│   ├── idl_agent.py       # Generates IDL specifications
│   └── test_agent.py      # Creates test suites
├── utils/                 # Utility functions
│   ├── file_handler.py    # Handles file operations
│   └── project_validator.py # Validates specifications
├── workflows/             # Workflow definitions
│   └── project_workflow.py # Main project generation workflow
└── main.py               # Entry point
```
###  Destination directories
```
├── src/                          # tentative directory where source is generated and saved
├── generated_projects/           # directory with all generated projects
├── └── <Timestamped Directory>   # code from src is moved to this timestamped dir at the end
```

## Running the Project Generator

1. Create a project specification file (e.g., `spec.txt`) with your requirements. Example:
```txt
Build a simple command-line calculator application that supports basic arithmetic operations.
The calculator should:
1. Accept two numbers and an operation as input
2. Perform the requested calculation
3. Handle errors gracefully
```

2. Run the project generator:
```bash
python main.py spec.txt
```

## Output Directory Structure
Generated projects are saved in the `generated_projects` directory with the following structure:
```
generated_projects/
├── YYYY-MM-DD_HH-MM-SS/  # Timestamp-based project folder
│   ├── src/              # Source code
│   ├── tests/            # Test files
│   ├── docs/             # Documentation
│   ├── README.md         # Project documentation
│   └── generation_summary.txt  # Generation details
```

## Adding New Features
After the initial project generation, you can add new features:

1. When prompted "Would you like to add more features?", type 'yes'
2. Enter your feature description when prompted
3. The generator will create new files or update existing ones in a new timestamped directory

## Troubleshooting

1. If you see an error about missing API key:
   - Verify that your `.env` file exists and contains the OPENAI_API_KEY
   - Ensure the API key is valid and has sufficient credits

2. If the generation process fails:
   - Check the `project_generation.log` file for detailed error messages
   - Verify that your specification file exists and is properly formatted

3. For other issues:
   - Review the console output for error messages
   - Check the generated_projects directory for partial outputs
