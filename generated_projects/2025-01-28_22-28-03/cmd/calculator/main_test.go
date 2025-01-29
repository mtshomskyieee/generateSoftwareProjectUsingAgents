package main

import (
    "fmt"
    "testing"
    "time"
)

// Test suite for the Calculator

// TestAdd tests the addition operation.
func TestAdd(t *testing.T) {
    calculator := NewCalculator()
    request := CalculationRequest{Operand1: 3, Operand2: 2, Operation: "add"}
    result, err := calculator.Calculate(request)

    if err != nil {
        t.Errorf("Expected no error, got %v", err)
    }
    if result.Result != 5 {
        t.Errorf("Expected result 5, got %f", result.Result)
    }
    if len(calculator.GetHistory()) == 0 {
        t.Errorf("Expected history length 1, got %d", len(calculator.GetHistory()))
    }
}

// TestSubtract tests the subtraction operation.
func TestSubtract(t *testing.T) {
    calculator := NewCalculator()
    request := CalculationRequest{Operand1: 5, Operand2: 3, Operation: "subtract"}
    result, err := calculator.Calculate(request)

    if err != nil {
        t.Errorf("Expected no error, got %v", err)
    }
    if result.Result != 2 {
        t.Errorf("Expected result 2, got %f", result.Result)
    }
}

// TestMultiply tests the multiplication operation.
func TestMultiply(t *testing.T) {
    calculator := NewCalculator()
    request := CalculationRequest{Operand1: 4, Operand2: 5, Operation: "multiply"}
    result, err := calculator.Calculate(request)

    if err != nil {
        t.Errorf("Expected no error, got %v", err)
    }
    if result.Result != 20 {
        t.Errorf("Expected result 20, got %f", result.Result)
    }
}

// TestDivide tests the division operation.
func TestDivide(t *testing.T) {
    calculator := NewCalculator()
    request := CalculationRequest{Operand1: 10, Operand2: 2, Operation: "divide"}
    result, err := calculator.Calculate(request)

    if err != nil {
        t.Errorf("Expected no error, got %v", err)
    }
    if result.Result != 5 {
        t.Errorf("Expected result 5, got %f", result.Result)
    }
}

// TestDivideByZero tests the division by zero error handling.
func TestDivideByZero(t *testing.T) {
    calculator := NewCalculator()
    request := CalculationRequest{Operand1: 10, Operand2: 0, Operation: "divide"}
    _, err := calculator.Calculate(request)

    if err == nil {
        t.Error("Expected division by zero error, got none")
    }
    if _, ok := err.(DivisionByZeroError); !ok {
        t.Errorf("Expected DivisionByZeroError, got %T", err)
    }
}

// TestInvalidOperation tests the error handling for invalid operations.
func TestInvalidOperation(t *testing.T) {
    calculator := NewCalculator()
    request := CalculationRequest{Operand1: 10, Operand2: 5, Operation: "invalid"}
    _, err := calculator.Calculate(request)

    if err == nil {
        t.Error("Expected error for invalid operation, got none")
    }
}

// TestClearHistory tests the functionality of clearing history.
func TestClearHistory(t *testing.T) {
    calculator := NewCalculator()
    request := CalculationRequest{Operand1: 10, Operand2: 5, Operation: "add"}
    _, _ = calculator.Calculate(request)

    // Ensure history is not empty
    if len(calculator.GetHistory()) == 0 {
        t.Error("Expected non-empty history before clearing")
    }

    calculator.ClearHistory()
    // Check after clearing
    if len(calculator.GetHistory()) != 0 {
        t.Error("Expected empty history after clearing")
    }
}

// TestGetHistory tests the retrieval of calculation history.
func TestGetHistory(t *testing.T) {
    calculator := NewCalculator()
    request1 := CalculationRequest{Operand1: 1, Operand2: 1, Operation: "add"}
    request2 := CalculationRequest{Operand1: 2, Operand2: 1, Operation: "subtract"}
    
    _, _ = calculator.Calculate(request1)
    _, _ = calculator.Calculate(request2)

    history := calculator.GetHistory()
    if len(history) != 2 {
        t.Errorf("Expected history length 2, got %d", len(history))
    }
    
    if history[0].Request.Operation != "add" || history[1].Request.Operation != "subtract" {
        t.Error("History does not match expected operations")
    }
}

// TestBoundaryConditions tests edge case scenarios, e.g., large numbers.
func TestBoundaryConditions(t *testing.T) {
    calculator := NewCalculator()
    request := CalculationRequest{Operand1: 1e308, Operand2: 1e308, Operation: "add"}
    
    result, err := calculator.Calculate(request)
    if err != nil {
        t.Errorf("Expected no error for large addition, got %v", err)
    }
    if result.Result != 2e308 {
        t.Errorf("Expected result %e, got %e", 2e308, result.Result)
    }
}

func main() {
    // Run tests
    t := new(testing.T)
    TestAdd(t)
    TestSubtract(t)
    TestMultiply(t)
    TestDivide(t)
    TestDivideByZero(t)
    TestInvalidOperation(t)
    TestClearHistory(t)
    TestGetHistory(t)
    TestBoundaryConditions(t)

    // Report any errors
    if t.Failed() {
        fmt.Println("Tests failed.")
    } else {
        fmt.Println("All tests passed.")
    }
}