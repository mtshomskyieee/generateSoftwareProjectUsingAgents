import unittest
from src.calculator import Calculator, DivisionByZeroError, InvalidOperationError, Calculation, HistoryEntry

class TestCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a Calculator instance for testing."""
        self.calculator = Calculator()

    def test_addition(self):
        """Test the addition operation."""
        result = self.calculator.calculate(2, 3, '+')
        self.assertEqual(result, 5)

    def test_subtraction(self):
        """Test the subtraction operation."""
        result = self.calculator.calculate(5, 3, '-')
        self.assertEqual(result, 2)

    def test_multiplication(self):
        """Test the multiplication operation."""
        result = self.calculator.calculate(4, 5, '*')
        self.assertEqual(result, 20)

    def test_division(self):
        """Test the division operation."""
        result = self.calculator.calculate(10, 2, '/')
        self.assertEqual(result, 5)

    def test_division_by_zero(self):
        """Test division by zero raises DivisionByZeroError."""
        with self.assertRaises(DivisionByZeroError):
            self.calculator.calculate(10, 0, '/')

    def test_invalid_operation(self):
        """Test invalid operation raises InvalidOperationError."""
        with self.assertRaises(InvalidOperationError):
            self.calculator.calculate(10, 5, '^')

    def test_empty_history(self):
        """Test that history is empty on initialization."""
        history = self.calculator.getHistory()
        self.assertEqual(len(history.entries), 0)

    def test_add_entry_to_history(self):
        """Test that a calculation can be added to history."""
        calculation = Calculation(1, 2, '+', 3)
        timestamp = "2023-01-01 12:00:00"
        entry = HistoryEntry(calculation, timestamp)

        self.calculator.history.add_entry(entry)

        self.assertEqual(len(self.calculator.history.entries), 1)
        self.assertEqual(self.calculator.history.entries[0].calculation.result, 3)
        self.assertEqual(self.calculator.history.entries[0].timestamp, timestamp)

    def test_edge_case_large_numbers(self):
        """Test addition with large numbers."""
        result = self.calculator.calculate(1e+18, 1e+18, '+')
        self.assertEqual(result, 2e+18)

    def test_edge_case_negative_numbers(self):
        """Test addition with negative numbers."""
        result = self.calculator.calculate(-5, -3, '+')
        self.assertEqual(result, -8)

    def test_edge_case_float_numbers(self):
        """Test addition with float numbers."""
        result = self.calculator.calculate(2.5, 3.5, '+')
        self.assertEqual(result, 6.0)

if __name__ == '__main__':
    unittest.main()