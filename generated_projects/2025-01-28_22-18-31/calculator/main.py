from datetime import datetime
from typing import List, Dict, Any


class DivisionByZeroError(Exception):
    """Exception raised for division by zero errors."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class CalculationHistory:
    """Represents a record of a calculation operation."""
    
    def __init__(self, operation: str, operand1: float, operand2: float, result: float):
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result
        self.timestamp = datetime.now().isoformat()  # Store the current timestamp

    def to_dict(self) -> Dict[str, Any]:
        """Converts the CalculationHistory object to a dictionary for easier access."""
        return {
            "operation": self.operation,
            "operand1": self.operand1,
            "operand2": self.operand2,
            "result": self.result,
            "timestamp": self.timestamp,
        }


class Calculator:
    """Calculator class to perform arithmetic operations and maintain a history."""
    
    def __init__(self):
        self.history: List[CalculationHistory] = []

    def calculate(self, operand1: float, operand2: float, operation: str) -> float:
        """Performs a calculation based on the provided operation.

        Args:
            operand1 (float): The first operand.
            operand2 (float): The second operand.
            operation (str): The operation to perform ("+", "-", "*", "/").

        Raises:
            DivisionByZeroError: If there is an attempt to divide by zero.

        Returns:
            float: The result of the operation.
        """
        if operation == "+":
            result = operand1 + operand2
        elif operation == "-":
            result = operand1 - operand2
        elif operation == "*":
            result = operand1 * operand2
        elif operation == "/":
            if operand2 == 0:
                raise DivisionByZeroError("Division by zero is not allowed.")
            result = operand1 / operand2
        else:
            raise ValueError(f"Unknown operation '{operation}'. Supported operations are '+', '-', '*', '/'.")
        
        # Record the calculation in history
        self.history.append(CalculationHistory(operation, operand1, operand2, result))
        return result

    def run(self) -> None:
        """Starts the calculator's main loop for user interaction."""
        while True:
            try:
                operand1 = float(input("Enter first operand (or 'q' to quit): "))
                operand2 = float(input("Enter second operand: "))
                operation = input("Enter operation (+, -, *, /): ")

                result = self.calculate(operand1, operand2, operation)
                print(f"Result: {result}")

            except ValueError as e:
                print(f"Input error: {e}")
            except DivisionByZeroError as e:
                print(f"Error: {e.message}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

            exit_prompt = input("Would you like to perform another calculation? (y/n): ")
            if exit_prompt.lower() != 'y':
                break

    def get_history(self) -> List[Dict[str, Any]]:
        """Retrieves the history of calculations performed.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing calculation histories.
        """
        return [entry.to_dict() for entry in self.history]


if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()
