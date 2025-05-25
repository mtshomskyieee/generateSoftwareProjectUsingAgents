import datetime

# Constants for operations
ADD = '+'
SUBTRACT = '-'
MULTIPLY = '*'
DIVIDE = '/'

class DivisionByZeroError(Exception):
    """Exception raised for division by zero errors."""
    def __init__(self, message: str, operation: str):
        self.message = message
        self.operation = operation
        super().__init__(self.message)

class InvalidInputError(Exception):
    """Exception raised for invalid input errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class Calculation:
    """Data structure for a calculation."""
    def __init__(self, num1: float, num2: float, operation: str, result: float):
        self.num1 = num1
        self.num2 = num2
        self.operation = operation
        self.result = result
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS

class HistoryEntry:
    """Data structure for a history entry."""
    def __init__(self, calculation: Calculation, description: str):
        self.calculation = calculation
        self.description = description

class Calculator:
    """Simple command-line calculator."""
    
    def __init__(self):
        self.history = []

    def run(self) -> None:
        """Start the calculator."""
        while True:
            try:
                user_input = input("Enter first number (or 'exit' to quit): ")
                if user_input.lower() == 'exit':
                    print("Calculator successfully exited.")
                    break 
                num1 = self.get_numeric_input(user_input)

                num2 = self.get_numeric_input(input("Enter second number: "))
                operation = input("Enter operation (+, -, *, /): ")
                self.validate_operation(operation)

                result = self.calculate(num1, num2, operation)
                self.display_result(result)

                calculation = Calculation(num1, num2, operation, result)
                self.log_history(calculation)

            except (ValueError, InvalidInputError) as e:
                print(f"Error: {e.message}")
            except DivisionByZeroError as e:
                print(f"Error: {e.message} in operation {e.operation}")

    def get_numeric_input(self, user_input: str) -> float:
        """Helper function to get numeric input from the user."""
        try:
            return float(user_input)
        except ValueError:
            raise InvalidInputError(f"Invalid input '{user_input}'. Please enter a numeric value.")

    def validate_operation(self, operation: str) -> None:
        """Ensure the operation is one of the allowed symbols."""
        if operation not in (ADD, SUBTRACT, MULTIPLY, DIVIDE):
            raise InvalidInputError(f"Invalid operation '{operation}' provided. Allowed operations are +, -, *, /.")

    def calculate(self, num1: float, num2: float, operation: str) -> float:
        """Perform calculation based on the provided operation."""
        operations = {
            ADD: lambda x, y: x + y,
            SUBTRACT: lambda x, y: x - y,
            MULTIPLY: lambda x, y: x * y,
            DIVIDE: lambda x, y: self.divide(x, y)
        }
        if operation not in operations:
            raise InvalidInputError(f"Invalid operation '{operation}'. Allowed operations are +, -, *, /.")
        return operations[operation](num1, num2)

    def divide(self, num1: float, num2: float) -> float:
        """Perform division operation, raises error for division by zero."""
        if num2 == 0:
            raise DivisionByZeroError("Division by zero is not allowed.", DIVIDE)
        return num1 / num2

    def display_result(self, result: float) -> None:
        """Display the result of the calculation."""
        print(f"Result: {result:.2f}")

    def log_history(self, calculation: Calculation) -> None:
        """Log the calculation history."""
        description = f"{calculation.num1} {calculation.operation} {calculation.num2} = {calculation.result}"
        history_entry = HistoryEntry(calculation, description)
        self.history.append(history_entry)
        print(f"History updated: {description}")

    def get_history(self) -> str:
        """Return a formatted string of the calculation history."""
        formatted_history = "\n".join(entry.description for entry in self.history)
        return formatted_history if formatted_history else "No calculation history."

if __name__ == "__main__":
    calc = Calculator()
    calc.run()