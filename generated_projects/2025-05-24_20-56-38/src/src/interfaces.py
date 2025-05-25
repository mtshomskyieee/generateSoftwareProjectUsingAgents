// Data Structures  
struct Calculation {  
    float operand1;  
    float operand2;  
    string operation;  
    float result;  
}  

struct HistoryEntry {  
    Calculation calculation;  
    string timestamp;  
}  

struct History {  
    list<HistoryEntry> entries;  
}  

// Interface Definitions  
interface Calculator {  
    // Method to run the calculator application  
    void run();  

    // Method to perform calculation  
    float calculate(float operand1, float operand2, string operation) throws DivisionByZeroError;  

    // Method to exit the calculator  
    void exit();  

    // Method to get calculation history  
    History getHistory();  
}  

// Type Definitions  
typedef float Number;  
typedef string Operation;  
typedef list<HistoryEntry> HistoryList;  

// Error Specifications  
exception DivisionByZeroError {  
    string message;  
    float operand1;  
    float operand2;  
}  

exception InvalidOperationError {  
    string message;  
    string operation;  
}