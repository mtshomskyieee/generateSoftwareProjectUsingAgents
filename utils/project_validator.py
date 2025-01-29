class ProjectValidator:
    @staticmethod
    def validate_specification(spec):
        """
        Validates the project specification format and content.
        Checks for required components and minimum content requirements.
        """
        if not isinstance(spec, str):
            raise ValueError("Specification must be a string")

        if len(spec.strip()) < 10:
            raise ValueError("Specification is too short to be valid")

        required_sections = ['should', 'must', 'will', 'application']
        has_requirements = any(word in spec.lower() for word in required_sections)
        if not has_requirements:
            raise ValueError("Specification must contain clear requirements (using words like 'should', 'must', 'will')")

        return True

    @staticmethod
    def validate_generated_code(code):
        """
        Performs basic validation on generated code.
        Checks for syntax and content validity.
        """
        if not isinstance(code, str):
            raise ValueError("Generated code must be a string")

        if not code.strip():
            raise ValueError("Generated code cannot be empty")

        # Check for basic Python syntax elements
        code_markers = ['class', 'def', 'import', 'from']
        has_code_structure = any(marker in code for marker in code_markers)
        if not has_code_structure:
            raise ValueError("Generated code must contain valid Python structures")

        return True

    @staticmethod
    def validate_idl_output(idl):
        """
        Validates the IDL specification output.
        Ensures it contains required IDL components.
        """
        if not isinstance(idl, str):
            raise ValueError("IDL specification must be a string")

        required_elements = ['struct', 'interface', 'typedef', 'exception']
        for element in required_elements:
            if element not in idl:
                raise ValueError(f"IDL specification must contain {element} definitions")

        return True