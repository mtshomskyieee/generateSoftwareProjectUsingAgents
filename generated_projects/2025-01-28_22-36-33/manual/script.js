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