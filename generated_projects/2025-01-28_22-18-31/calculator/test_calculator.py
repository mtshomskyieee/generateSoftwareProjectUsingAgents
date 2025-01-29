import unittest
from main import Calculator, DivisionByZeroError

class TestCalculator(unittest.TestCase):

    def setUp(self):
        """Set up the calculator instance for tests."""
        self.calculator = Calculator()

    def test_addition(self):
        """Test addition operation."""
        result = self.calculator.calculate(1, 2, "+")
        self.assertEqual(result, 3)

    def test_subtraction(self):
        """Test subtraction operation."""
        result = self.calculator.calculate(5, 3, "-")
        self.assertEqual(result, 2)

    def test_multiplication(self):
        """Test multiplication operation."""
        result = self.calculator.calculate(4, 7, "*")
        self.assertEqual(result, 28)

    def test_division(self):
        """Test division operation."""
        result = self.calculator.calculate(10, 2, "/")
        self.assertEqual(result, 5)

    def test_division_by_zero(self):
        """Test division by zero raises DivisionByZeroError."""
        with self.assertRaises(DivisionByZeroError):
            self.calculator.calculate(10, 0, "/")

    def test_unknown_operation(self):
        """Test passing an unknown operation raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.calculate(10, 5, "%")

    def test_history_recording(self):
        """Test calculation history stores results correctly."""
        self.calculator.calculate(1, 1, "+")
        history = self.calculator.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['operation'], '+')
        self.assertEqual(history[0]['operand1'], 1)
        self.assertEqual(history[0]['operand2'], 1)
        self.assertEqual(history[0]['result'], 2)

    def test_empty_history(self):
        """Test retrieving history before any calculations."""
        history = self.calculator.get_history()
        self.assertEqual(history, [])

    def test_run_method(self):
        """Test run method for user interactions (mocked)."""
        import builtins
        original_input = builtins.input
        
        # Mock inputs for run method
        inputs = iter(["1", "2", "+", "y", "3", "0", "/", "n"])
        builtins.input = lambda _: next(inputs)
        
        with self.assertRaises(DivisionByZeroError):
            self.calculator.run()

        # Restore original input
        builtins.input = original_input

    # Edge cases
    def test_large_numbers_addition(self):
        """Test addition with large numbers."""
        result = self.calculator.calculate(1e10, 1e10, "+")
        self.assertEqual(result, 2e10)

    def test_negative_subtraction(self):
        """Test subtraction resulting in a negative number."""
        result = self.calculator.calculate(3, 5, "-")
        self.assertEqual(result, -2)

    def test_decimal_multiplication(self):
        """Test multiplication with decimal numbers."""
        result = self.calculator.calculate(1.5, 2.5, "*")
        self.assertEqual(result, 3.75)

    def test_integer_division(self):
        """Test division with integer result."""
        result = self.calculator.calculate(6, 3, "/")
        self.assertEqual(result, 2)

if __name__ == "__main__":
    unittest.main()
