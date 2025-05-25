# Calculator Application Documentation

## Table of Contents
1. [Installation and Setup](#installation-and-setup)
2. [Available Operations](#available-operations)
3. [Usage Examples](#usage-examples)
4. [Error Handling Guide](#error-handling-guide)
5. [History Feature Usage](#history-feature-usage)

---

## 1. Installation and Setup

To install and set up the command-line calculator application, follow these steps:

1. Ensure you have Python installed on your system. This application is compatible with Python 3.x. You can download it from the official [Python website](https://www.python.org/downloads/).
   
2. Clone the repository or download the source code to your local machine. If you are using Git, execute the following command in your terminal:
   ```bash
   git clone https://github.com/yourusername/calculator.git
   ```

3. Navigate to the project directory:
   ```bash
   cd calculator
   ```

4. Install any required dependencies (if any). For this application, there are no external libraries needed, as it uses only built-in libraries.

5. You can now run the application with:
   ```bash
   python calculator.py
   ```

---

## 2. Available Operations

The calculator supports the following basic arithmetic operations:

- **Addition (`+`)**: Adds two numbers together.
- **Subtraction (`-`)**: Subtracts the second number from the first.
- **Multiplication (`*`)**: Multiplies two numbers.
- **Division (`/`)**: Divides the first number by the second; division by zero is handled gracefully.

---

## 3. Usage Examples

### Example 1: Basic Operations

To perform calculations interactively, run the application using the command:
```bash
python calculator.py
```

You will be prompted to input the first number, second number, and the arithmetic operation. 

**Interactive Session:**
```plaintext
Enter the first number (or type 'exit' to quit): 8
Enter the second number: 2
Enter operation (+, -, *, /): /
The result of 8.0 / 2.0 = 4.0
```

### Example 2: Continuous Calculations
You can continue making calculations until you choose to exit:
```plaintext
Enter the first number (or type 'exit' to quit): 10
Enter the second number: 5
Enter operation (+, -, *, /): +
The result of 10.0 + 5.0 = 15.0

Enter the first number (or type 'exit' to quit): 20
Enter the second number: 4
Enter operation (+, -, *, /): -
The result of 20.0 - 4.0 = 16.0
```

### Example 3: Exiting the Application
You may type 'exit' at any prompt to terminate the program:
```plaintext
Enter the first number (or type 'exit' to quit): exit
Exiting the calculator. Thank you for using it!
```

---

## 4. Error Handling Guide

The calculator provides error handling for the following scenarios:

1. **Division by Zero**:
   - If you try to divide a number by zero, you will see:
     ```plaintext
     Division by zero is not allowed.
     ```

2. **Invalid Operations**:
   - If you input an operation that is not supported, such as `^`, you will receive:
     ```plaintext
     Invalid operation: ^
     ```

3. **Invalid Input**:
   - In case you enter non-numeric values, such as letters, the calculator will output:
     ```plaintext
     invalid literal for float(): <input_value>
     ```

---

## 5. History Feature Usage

The calculator maintains a history of calculations during the run time, which can be accessed after performing calculations.

- Each entry includes:
  - Operand 1
  - Operand 2
  - Operation
  - Result
  - Timestamp of when the calculation was made

To view your calculation history, you can extend the application to print all the entries stored in `self.history.entries`.

**Example of Printing History (to be implemented):**
```plaintext
Calculation History:
1. 10 + 5 = 15 [Timestamp]
2. 20 - 4 = 16 [Timestamp]
```

---

With this documentation, you should be fully equipped to install, use, and troubleshoot the command-line calculator application effectively. If any errors arise, refer to the error handling guide to understand and resolve them promptly. Happy calculating!