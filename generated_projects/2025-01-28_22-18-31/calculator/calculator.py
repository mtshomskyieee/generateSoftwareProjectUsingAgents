// Data Structures
struct CalculationHistory {
    string operation;        // The arithmetic operation performed (e.g., "+", "-", "*", "/")
    float operand1;         // The first operand in the calculation
    float operand2;         // The second operand in the calculation
    float result;           // The result of the calculation
    string timestamp;       // The timestamp of when the calculation was performed
}

// Interface Definitions
interface Calculator {
    // Method to perform a calculation
    float calculate(float operand1, float operand2, string operation) raises(DivisionByZeroError);

    // Method to run the calculator loop
    void run();

    // Method to retrieve the calculation history
    sequence<CalculationHistory> getHistory();
}

// Type Definitions
typedef float Number;
typedef string Operation;

// Error Specifications
exception DivisionByZeroError {
    string message;         // Descriptive error message
};