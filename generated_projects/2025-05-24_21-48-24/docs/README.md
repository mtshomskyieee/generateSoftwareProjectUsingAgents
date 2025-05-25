# Command-Line Calculator Documentation

Welcome to the documentation for the command-line calculator built in Python. This application supports basic arithmetic operations and maintains a history of calculations. Below you will find detailed instructions to help you get started, along with usage examples and information on error handling.

## 1. Installation and Setup

To install and run the calculator, follow these steps:

### Prerequisites

- Python 3.x must be installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

### Steps to Install

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Navigate to the directory** where the calculator script is located.

3. **Run the application**:
   You can execute the calculator directly using a command line interface:
   ```bash
   python calculator.py
   ```

## 2. Available Operations

The calculator supports the following basic arithmetic operations:

- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Division (`/`)

### Operation Breakdown

- **Addition**: `num1 + num2`
- **Subtraction**: `num1 - num2`
- **Multiplication**: `num1 * num2`
- **Division**: `num1 / num2` (Note: Be cautious of division by zero)

## 3. Usage Examples

To perform calculations, the application prompts you to input two numbers and an operation:

### Example 1: Addition
```plaintext
Enter first number (or 'exit' to quit): 5
Enter second number: 3
Enter operation (+, -, *, /): +
Result: 8.00
History updated: 5.0 + 3.0 = 8.0
```

### Example 2: Division
```plaintext
Enter first number (or 'exit' to quit): 6
Enter second number: 3
Enter operation (+, -, *, /): /
Result: 2.00
History updated: 6.0 / 3.0 = 2.0
```

### Example 3: Continuous Operations
You can continuously perform calculations until you choose to exit the application by entering 'exit':
```plaintext
Enter first number (or 'exit' to quit): exit
```

## 4. Error Handling Guide

The calculator is designed to handle errors gracefully. Here are a few common errors and how they are managed:

### **Division by Zero**
If you try to divide by zero, an error message will be shown:
```plaintext
Error: Division by zero is not allowed. in operation /
```

### **Invalid Input**
If an invalid input is provided (e.g., a letter instead of a number), an error message will appear:
```plaintext
Error: Invalid input with value a
```

### **Invalid Operation**
If an operation outside of the supported operations is entered:
```plaintext
Error: Invalid operation
```

Make sure to enter valid numbers and operations to avoid these issues.

## 5. History Feature Usage

The calculator maintains a history of your calculations, allowing you to view the results of previous operations.

### Accessing History
You can retrieve the calculation history using the `getHistory` method. Each entry contains the two numbers, the operation, the result, and the timestamp of the calculation.

### Example of History Entry
A history entry will look like this:
```plaintext
5.0 + 3.0 = 8.0
```

To view history, modify the code in the `Calculator` class for a history display function.

### Clear History
Currently, the implementation does not support clearing history. If needed, this feature can be added to enhance the application.

## Conclusion

This command-line calculator is a simple yet powerful tool for performing basic arithmetic operations. With its clear instructions, error handling, and history feature, it is user-friendly and efficient for anyone looking for quick calculations. For any issues or feature requests, consider contributing to the codebase or reaching out for support. Happy calculating!