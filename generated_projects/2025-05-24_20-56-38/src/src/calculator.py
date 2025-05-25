from datetime import datetime
from enum import Enum

class DivisionByZeroError(Exception):
    """Exception raised for division by zero errors."""
    def __init__(self, operand1: float, operand2: float):
        self.message = f"Division by zero is not allowed when dividing {operand1} by {operand2}."
        self.operand1 = operand1
        self.operand2 = operand2
        super().__init__(self.message)

class InvalidOperationError(Exception):
    """Exception raised for invalid operation errors."""
    def __init__(self, operation: str):
        self.message = f"Invalid operation: '{operation}'. Please use one of the following: +, -, *, /."
        self.operation = operation
        super().__init__(self.message)

class Operation(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"

class Calculation:
    """Data structure to hold a single calculation, including operands, operation, and result.
    
    Attributes:
        operand1 (float): The first operand.
        operand2 (float): The second operand.
        operation (str): The mathematical operation performed.
        result (float): The result of the calculation.
    """
    def __init__(self, operand1: float, operand2: float, operation: str, result: float):
        self.operand1 = operand1
        self.operand2 = operand2
        self.operation = operation
        self.result = result

class HistoryEntry:
    """Data structure for holding a calculation history entry, including a calculation and timestamp.
    
    Attributes:
        calculation (Calculation): The calculation performed.
        timestamp (datetime): The time when the calculation was performed.
    """
    def __init__(self, calculation: Calculation, timestamp: datetime):
        self.calculation = calculation
        self.timestamp = timestamp

class History:
    """Container for maintaining calculation history."""
    def __init__(self):
        self.entries = []

    def add_entry(self, entry: HistoryEntry) -> None:
        """Add a calculation entry to the history."""
        self.entries.append(entry)

    def get_entries(self):
        """Retrieve all entries from the calculation history."""
        return self.entries[:]

    def clear_history(self) -> None:
        """Clear all entries from the history."""
        self.entries.clear()

class Calculator:
    """Calculator interface implementation handling calculations and their history."""
    def __init__(self):
        self.history = History()

    def run(self) -> None:
        """Main loop of the calculator application. Handles user input and calls calculation methods."""
        while True:
            user_input = input("Enter the first number (or type 'exit' to quit): ")
            if user_input.lower() == 'exit':
                print("Exiting the calculator. Thank you for using it!")
                break

            try:
                operand1 = self.get_float_input("Enter the first number: ")
                operand2 = self.get_float_input("Enter the second number: ")
                operation = input("Enter operation (+, -, *, /): ")

                result = self.calculate(operand1, operand2, operation)
                print(f"The result of {operand1} {operation} {operand2} = {result}")

                # Record the calculation and its timestamp in history
                timestamp = datetime.now()
                calculation = Calculation(operand1, operand2, operation, result)
                entry = HistoryEntry(calculation, timestamp)
                self.history.add_entry(entry)

            except ValueError as e:
                print(f"Error: {e}")
            except InvalidOperationError as e:
                print(f"Error: {e.message}")
            except DivisionByZeroError as e:
                print(f"Error: {e.message}")

    def get_float_input(self, prompt: str) -> float:
        """Prompt user for a float input and handle invalid input gracefully.
        
        Args:
            prompt (str): The prompt message to display for user input.
        
        Returns:
            float: The user input converted to a float.
        
        Raises:
            ValueError: If the user input cannot be converted to a float.
        """
        while True:
            user_input = input(prompt)
            try:
                return float(user_input)
            except ValueError:
                print(f"Invalid input '{user_input}'. Please enter a valid number.")

    def calculate(self, operand1: float, operand2: float, operation: str) -> float:
        """Perform the requested calculation based on input operands and operation.
        
        Args:
            operand1 (float): The first operand.
            operand2 (float): The second operand.
            operation (str): The operation to perform.
        
        Returns:
            float: The result of the calculation.
        
        Raises:
            DivisionByZeroError: If an attempt is made to divide by zero.
            InvalidOperationError: If the operation is not recognized.
        """
        if operation == Operation.ADD.value:
            return operand1 + operand2
        elif operation == Operation.SUBTRACT.value:
            return operand1 - operand2
        elif operation == Operation.MULTIPLY.value:
            return operand1 * operand2
        elif operation == Operation.DIVIDE.value:
            if operand2 == 0:
                raise DivisionByZeroError(operand1, operand2)
            return operand1 / operand2
        else:
            raise InvalidOperationError(operation)

    def get_history(self) -> History:
        """Return the history of calculations."""
        return self.history

if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()