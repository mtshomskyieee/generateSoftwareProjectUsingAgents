# Calculator Application Documentation

## 1. Installation and Setup

To install and set up the Calculator application, follow these steps:

### Prerequisites
- Ensure that you have [Go](https://golang.org/dl/) installed on your machine. You can download the installer that suits your operating system.

### Steps
1. **Clone the Repository**  
   Run the following command in your terminal to clone the repository:
   ```bash
   git clone https://your-repository-url.git
   ```
   
2. **Navigate to the Project Directory**  
   Change to the project’s directory:
   ```bash
   cd calculator-application
   ```

3. **Build the Application**  
   Build the application using the Go build command:
   ```bash
   go build -o calculator
   ```
   
4. **Run the Application**  
   Start the application:
   ```bash
   ./calculator
   ```

## 2. Available Operations

The calculator supports the following operations:

- **Addition**: `add`
- **Subtraction**: `subtract`
- **Multiplication**: `multiply`
- **Division**: `divide`

## 3. Usage Examples

### Basic Calculations
To perform a calculation, the application will prompt you for two numbers and the desired operation. Here are a few examples:

- **Add**:
   - Input: `3`, `5`, `add`
   - Output: `Result: 8`

- **Subtract**:
   - Input: `10`, `4`, `subtract`
   - Output: `Result: 6`

- **Multiply**:
   - Input: `6`, `7`, `multiply`
   - Output: `Result: 42`

- **Divide**:
   - Input: `12`, `4`, `divide`
   - Output: `Result: 3`

### Handling Division by Zero
If you attempt to divide by zero:
- **Input**: `10`, `0`, `divide`
- **Output**: `Error: Division by zero is not allowed!`

## 4. Error Handling Guide

### Common Errors
1. **Division by Zero**
   - When attempting to divide by zero, the application will return an error.
  
2. **Invalid Operation**
   - If an operation is entered that is not supported, the application will return an error.

### Error Messages
- Division by zero: "Error: Division by zero is not allowed!"
- Invalid operation: "Error: Invalid operation provided!"

## 5. History Feature Usage

The calculator maintains a history of all calculations performed during the session. To access the history:

1. **View History**: The calculator will automatically display a list of calculations once a calculation is completed.
   
2. **Clearing History**: If you wish to clear the history, you can invoke the clear history command. This will reset the history list to empty.

### Example of History Access
After performing calculations:
- Inputs: 
    1. `3`, `2`, `add`
    2. `5`, `2`, `subtract`
   
- Output: 
```
History:
1. 3 + 2 = 5
2. 5 - 2 = 3
```

### Clearing History Example
To clear the history:
- Input: `clear history`
- Output: `History cleared successfully.`

This documentation provides a clear and concise understanding of how to install, use, and troubleshoot the Calculator application. It allows users to leverage its full capabilities in performing basic arithmetic operations while maintaining a record of their calculations.