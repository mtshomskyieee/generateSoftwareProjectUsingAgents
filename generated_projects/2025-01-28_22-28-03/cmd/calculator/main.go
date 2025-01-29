package main

import (
    "fmt"
    "time"
)

// Data Structures

// CalculationRequest represents a request for a calculation.
type CalculationRequest struct {
    Operand1  float64 `json:"operand1"`  // The first number for calculation
    Operand2  float64 `json:"operand2"`  // The second number for calculation
    Operation string  `json:"operation"` // The arithmetic operation (add, subtract, multiply, divide)
}

// CalculationResult represents the result of a calculation.
type CalculationResult struct {
    Result  float64 `json:"result"`  // The result of the calculation
    Message string  `json:"message"` // A message indicating success or error
}

// CalculationHistory stores the request, result, and timestamp of calculations.
type CalculationHistory struct {
    Request   CalculationRequest   `json:"request"`   
    Result    CalculationResult    `json:"result"`    
    Timestamp string               `json:"timestamp"` // The time at which the calculation was performed
}

// Error Specifications

// DivisionByZeroError represents an error for division by zero scenario.
type DivisionByZeroError struct {
    Message  string  `json:"message"`  // Description of the division by zero error
    Operand1 float64 `json:"operand1"` // The first operand that caused the error
    Operand2 float64 `json:"operand2"` // The second operand that caused the error
}

// ICalculator interface defines calculator operations.
type ICalculator interface {
    // Calculate performs the calculation based on the given request.
    Calculate(request CalculationRequest) (CalculationResult, error)

    // GetHistory retrieves the calculation history.
    GetHistory() []CalculationHistory

    // ClearHistory clears the calculation history.
    ClearHistory()
}

// Calculator implements the ICalculator interface.
type Calculator struct {
    history []CalculationHistory // Stores the history of calculations
}

// NewCalculator initializes and returns a new Calculator instance.
func NewCalculator() *Calculator {
    return &Calculator{
        history: []CalculationHistory{},
    }
}

// Calculate performs a calculation based on the provided request.
func (c *Calculator) Calculate(request CalculationRequest) (CalculationResult, error) {
    var result float64
    var message string

    switch request.Operation {
    case "add":
        result = request.Operand1 + request.Operand2
        message = "Calculation successful."
    case "subtract":
        result = request.Operand1 - request.Operand2
        message = "Calculation successful."
    case "multiply":
        result = request.Operand1 * request.Operand2
        message = "Calculation successful."
    case "divide":
        if request.Operand2 == 0 {
            err := DivisionByZeroError{
                Message:  "Division by zero is not allowed.",
                Operand1: request.Operand1,
                Operand2: request.Operand2,
            }
            return CalculationResult{}, err
        }
        result = request.Operand1 / request.Operand2
        message = "Calculation successful."
    default:
        return CalculationResult{}, fmt.Errorf("invalid operation: %s", request.Operation)
    }
    
    // Create and save CalculationResult and CalculationHistory
    calcResult := CalculationResult{
        Result:  result,
        Message: message,
    }
    historyEntry := CalculationHistory{
        Request:   request,
        Result:    calcResult,
        Timestamp: time.Now().Format(time.RFC3339),
    }
    c.history = append(c.history, historyEntry)

    return calcResult, nil
}

// GetHistory retrieves the calculation history.
func (c *Calculator) GetHistory() []CalculationHistory {
    return c.history
}

// ClearHistory clears the calculation history.
func (c *Calculator) ClearHistory() {
    c.history = []CalculationHistory{}
}

func main() {
    // Example usage of the Calculator
    calculator := NewCalculator()

    // Performing calculations
    req1 := CalculationRequest{Operand1: 10, Operand2: 5, Operation: "add"}
    result1, err1 := calculator.Calculate(req1)
    if err1 == nil {
        fmt.Println("Result:", result1.Result)
    } else {
        fmt.Println("Error:", err1)
    }

    // Performing another calculation
    req2 := CalculationRequest{Operand1: 10, Operand2: 0, Operation: "divide"}
    result2, err2 := calculator.Calculate(req2)
    if err2 == nil {
        fmt.Println("Result:", result2.Result)
    } else {
        fmt.Println("Error:", err2)
    }

    // Get calculation history
    history := calculator.GetHistory()
    fmt.Println("Calculation History:", history)

    // Clear history
    calculator.ClearHistory()
    fmt.Println("History after clearing:", calculator.GetHistory())
}