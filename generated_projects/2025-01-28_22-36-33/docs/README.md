# Comprehensive Documentation for the Calculator Application

## Installation and Setup

To install the calculator application, follow these steps:

1. **Ensure you have a web browser**: The calculator runs on any modern web browser such as Chrome, Firefox, or Edge.

2. **Create the project structure**: Set up your project directory as follows:

   ```
   calculator/
        ├── index.html
        ├── style.css
        └── script.js
   ```

3. **Create the HTML file (`index.html`)**: Copy the following template into your `index.html` file.

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <link rel="stylesheet" href="style.css">
       <title>Calculator</title>
   </head>
   <body>
       <h1>Simple Calculator</h1>
       <div>
           <input type="number" id="num1" placeholder="Enter first number" required>
           <input type="number" id="num2" placeholder="Enter second number" required>
           <select id="operation">
               <option value="+">Add</option>
               <option value="-">Subtract</option>
               <option value="*">Multiply</option>
               <option value="/">Divide</option>
           </select>
           <button id="calculate">Calculate</button>
       </div>
       <h2>Result: <span id="result"></span></h2>
       <h3>History:</h3>
       <ul id="history"></ul>
       <script src="script.js"></script>
   </body>
   </html>
   ```

4. **Create the JavaScript file (`script.js`)**: This file contains the logic to perform calculations. Populate `script.js` with the following code:

   ```javascript
   class Calculation {
       constructor(number1, number2, operation) {
           this.number1 = number1;
           this.number2 = number2;
           this.operation = operation;
           this.result = null;
           this.formattedResult = "";
       }

       performCalculation() {
           switch (this.operation) {
               case '+':
                   this.result = this.number1 + this.number2;
                   this.formattedResult = `${this.number1} + ${this.number2} = ${this.result}`;
                   break;
               case '-':
                   this.result = this.number1 - this.number2;
                   this.formattedResult = `${this.number1} - ${this.number2} = ${this.result}`;
                   break;
               case '*':
                   this.result = this.number1 * this.number2;
                   this.formattedResult = `${this.number1} * ${this.number2} = ${this.result}`;
                   break;
               case '/':
                   if (this.number2 === 0) {
                       throw new DivisionByZeroError("Division by zero is not allowed.", this.number1, this.number2);
                   }
                   this.result = this.number1 / this.number2;
                   this.formattedResult = `${this.number1} / ${this.number2} = ${this.result}`;
                   break;
               default:
                   throw new ValueError(`Unsupported operation: ${this.operation}`);
           }
       }
   }

   class DivisionByZeroError extends Error {
       constructor(message, number1, number2) {
           super(message);
           this.number1 = number1;
           this.number2 = number2;
       }
   }

   class CalculationHistory {
       constructor() {
           this.entries = [];
       }

       addEntry(calculation) {
           this.entries.push(calculation);
       }

       clear() {
           this.entries = [];
       }
   }

   document.getElementById('calculate').addEventListener('click', function () {
       const num1 = parseFloat(document.getElementById('num1').value);
       const num2 = parseFloat(document.getElementById('num2').value);
       const operation = document.getElementById('operation').value;
       const resultField = document.getElementById('result');
       const historyField = document.getElementById('history');
       const history = new CalculationHistory();
       
       try {
           const calculation = new Calculation(num1, num2, operation);
           calculation.performCalculation();
           resultField.textContent = calculation.formattedResult;
           history.addEntry(calculation);
           const li = document.createElement('li');
           li.textContent = calculation.formattedResult;
           historyField.appendChild(li);
       } catch (error) {
           alert(error.message);
       }
   });
   ```

5. **Create the CSS file (`style.css`)**: Add this CSS for basic styling.

   ```css
   body {
       font-family: Arial, sans-serif;
       padding: 20px;
   }
   input, select {
       margin: 5px;
   }
   ```

## Available Operations

The calculator application currently supports the following basic arithmetic operations:

1. **Addition** (`+`)
2. **Subtraction** (`-`)
3. **Multiplication** (`*`)
4. **Division** (`/`)

## Usage Examples

1. **Addition Example**:  
   - Inputs: `5` and `3`, select `+`  
   - Output: `5 + 3 = 8`

2. **Subtraction Example**:  
   - Inputs: `10` and `7`, select `-`  
   - Output: `10 - 7 = 3`

3. **Multiplication Example**:  
   - Inputs: `4` and `5`, select `*`  
   - Output: `4 * 5 = 20`

4. **Division Example**:  
   - Inputs: `10` and `2`, select `/`  
   - Output: `10 / 2 = 5`

5. **Division by Zero**:  
   - Inputs: `10` and `0`, select `/`  
   - Output: Alert message: `Division by zero is not allowed.`

## Error Handling Guide

The application handles errors in the following ways:

- **Division by Zero**: If the user attempts to divide by zero, an alert will notify them with the message "Division by zero is not allowed."
- **Unsupported Operations**: If an unsupported operation is selected, an alert will indicate that it is not a valid operation (e.g., using `%`).

To prevent errors, ensure that numeric inputs are appropriately filled, and valid operations are selected.

## History Feature Usage

The application maintains a history of all calculations performed during the session:

- After each successful calculation, the formatted result will be appended to a list labeled "History".
- Users can refer to the history to view their past calculations.
- Currently, there is no clear history functionality implemented, but this can be added later by incorporating a `Clear History` button.

This documentation should provide comprehensive guidance for users to install, set up, and utilize the calculator application effectively.