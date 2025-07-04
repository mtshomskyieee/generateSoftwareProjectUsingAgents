import os
from datetime import datetime
import shutil
import os

class FileHandler:
    def __init__(self):
        self.base_output_dir = "generated_projects"

    def move_files(self, src_dir, dest_dir):
        # Ensure the destination directory exists
        os.makedirs(dest_dir, exist_ok=True)

        # Walk through the source directory
        for root, dirs, files in os.walk(src_dir):
            # Calculate the relative path from the source directory
            rel_path = os.path.relpath(root, src_dir)
            # Create the corresponding directory structure in the destination
            dest_path = os.path.join(dest_dir, rel_path)
            os.makedirs(dest_path, exist_ok=True)

            # Move each file
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_path, file)
                shutil.move(src_file, dest_file)
                print(f"Moved: {src_file} to {dest_file}")

    def cleanup_directories(self, src_dir):
            remaining_directories = [f for f in os.listdir(src_dir)]
            for d in remaining_directories:
                cleanup_dir = "/".join([src_dir, d])
                print(f"Move Cleanup: {src_dir}, removing {cleanup_dir}")
                shutil.rmtree(cleanup_dir,ignore_errors=True)

    def read_specification(self, file_path):
        """
        Reads and validates the project specification file.
        """
        with open(file_path, 'r') as file:
            content = file.read().strip()

        if not content:
            raise ValueError("Specification file is empty")

        return content

    def save_project_files(self, project_files):
        """
        Saves generated project files to disk in an organized structure.

        Directory structure:
        generated_projects/
        ├── YYYY-MM-DD_HH-MM-SS/  # Timestamp-based project folder
        │   ├── src/              # Source code
        │   ├── tests/            # Test files
        │   ├── docs/             # Documentation
        │   └── README.md         # Project documentation
        """
        # Create timestamp-based project directory
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        project_dir = os.path.join(self.base_output_dir, timestamp)

        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        for file_path, content in project_files.items():
            # Construct full path within project directory
            full_path = os.path.join(project_dir, file_path)

            # Create directory if it doesn't exist
            directory = os.path.dirname(full_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Save the file - convert content to string if needed
            with open(full_path, 'w') as file:
                if hasattr(content, 'raw_output'):  # Handle CrewOutput objects
                    file.write(str(content.raw_output))
                else:
                    file.write(str(content))  # Convert any other type to string

        # Create a summary file
        summary_path = os.path.join(project_dir, "generation_summary.txt")
        with open(summary_path, 'w') as f:
            f.write(f"Project generated at: {timestamp}\n")
            f.write("Generated files:\n")
            for file_path in project_files.keys():
                f.write(f"- {file_path}\n")

        # move source to the project directory
        src_directory = './src'
        self.move_files(src_directory, project_dir)
        self.cleanup_directories(src_directory)

        return project_dir