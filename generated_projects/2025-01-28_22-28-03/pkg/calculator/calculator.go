// Data Structures
struct CalculationRequest {
    // Properties with types
    float operand1;          // The first number for calculation
    float operand2;          // The second number for calculation
    string operation;        // The arithmetic operation (add, subtract, multiply, divide)
}

struct CalculationResult {
    // Properties with types
    float result;            // The result of the calculation
    string message;          // A message indicating success or error
}

struct CalculationHistory {
    // Properties with types
    CalculationRequest request;  // The request used for the calculation
    CalculationResult result;     // The result of the calculation
    string timestamp;             // The time at which the calculation was performed
}

// Interface Definitions
interface ICalculator {
    // Method signatures with parameters and return types
    
    // Method to perform a calculation
    CalculationResult calculate(in CalculationRequest request) raises (DivisionByZeroError);
    
    // Method to retrieve the calculation history
    list<CalculationHistory> getHistory();
    
    // Method to clear the calculation history
    void clearHistory();
}

// Type Definitions
typedef float FloatType;
typedef string OperationType; // Can represent "add", "subtract", "multiply", "divide"

// Error Specifications
exception DivisionByZeroError {
    // Error properties
    string message;          // Description of the division by zero error
    float operand1;          // The first operand that caused the error
    float operand2;          // The second operand that caused the error
}