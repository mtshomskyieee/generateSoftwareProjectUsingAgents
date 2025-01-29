# Calculator Application Documentation

## Installation and Setup

To set up and run the command-line calculator application written in Python, follow these steps:

### Prerequisites
- Ensure that Python (version 3.6 or higher) is installed on your machine.
- You can download Python from the [official website](https://www.python.org/downloads/).

### Steps to Install
1. **Download the Source Code**:
   - Clone the repository or download the source code ZIP file.

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Required Packages** (if any):
   - Typically, this application does not require external libraries, but if specified by the project, use pip to install them:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   - Navigate to the directory containing the calculator script and execute:

   ```bash
   python calculator.py
   ```

## Available Operations
The calculator supports the following basic arithmetic operations:
1. **Addition (+)**: Sums two numbers.
2. **Subtraction (-)**: Subtracts the second number from the first.
3. **Multiplication (*)**: Multiplies two numbers.
4. **Division (/)**: Divides the first number by the second (handles division by zero gracefully).

## Usage Examples
### Example 1: Basic Calculations
```bash
$ python calculator.py
Enter first number: 3
Enter second number: 5
Enter operation (+, -, *, /): +
Result: 8

Continue calculations? (y/n): y
Enter first number: 10
Enter second number: 0
Enter operation (+, -, *, /): /
Result: Division by zero is not allowed.
```

### Example 2: Continuous Calculation
```bash
$ python calculator.py
Enter first number: 15
Enter second number: 3
Enter operation (+, -, *, /): -
Result: 12

Continue calculations? (y/n): y
Enter first number: 4
Enter second number: 2
Enter operation (+, -, *, /): *
Result: 8

Continue calculations? (y/n): n
```

### Example 3: Error Handling
```bash
$ python calculator.py
Enter first number: 10
Enter second number: 0
Enter operation (+, -, *, /): /
Result: Division by zero is not allowed.
```

## Error Handling Guide
The calculator gracefully handles the following errors:
1. **Division by Zero**: If the user attempts to divide by zero, a friendly message is displayed instead of crashing.
2. **Unknown Operations**: If an unsupported operation is entered, a `ValueError` is raised informing the user of valid operations.

### Troubleshooting
- If the application does not run, ensure that Python is correctly installed and the script is being executed from the right directory.
- If you encounter issues with calculations, check the inputs for correctness (numbers only and valid operation symbols).

## History Feature Usage
The calculator maintains a history of calculations performed during the session. Each entry in the history includes:
- **Operand 1**: The first number.
- **Operand 2**: The second number.
- **Operation**: The operation performed.
- **Result**: The result of the calculation.

### Checking History
You can access the history anytime during the session, displaying all past operations and their results. This feature helps in tracking previous calculations for review or further calculations.

```bash
Enter first number: 5
Enter second number: 2
Enter operation (+, -, *, /): +
Result: 7

Enter 'h' to view history or any other key to continue: h
History:
1. 5 + 2 = 7
```

This comprehensive documentation serves to guide users in installing, using, and troubleshooting the command-line calculator application, ensuring an effective and user-friendly experience.