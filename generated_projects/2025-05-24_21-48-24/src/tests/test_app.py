import unittest
from src.app import Calculator, DivisionByZeroError, InvalidInputError, Calculation

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()
    
    def test_addition(self):
        result = self.calc.calculate(5, 3, '+')
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calc.calculate(5, 3, '-')
        self.assertEqual(result, 2)

    def test_multiplication(self):
        result = self.calc.calculate(5, 3, '*')
        self.assertEqual(result, 15)

    def test_division(self):
        result = self.calc.calculate(6, 3, '/')
        self.assertEqual(result, 2)

    def test_division_by_zero(self):
        with self.assertRaises(DivisionByZeroError) as context:
            self.calc.calculate(5, 0, '/')
        self.assertEqual(str(context.exception), "Division by zero is not allowed.")

    def test_invalid_operation(self):
        with self.assertRaises(InvalidInputError) as context:
            self.calc.calculate(5, 3, '%')
        self.assertEqual(str(context.exception), "Invalid operation")

    def test_log_history(self):
        self.calc.calculate(5, 3, '+')
        history = self.calc.getHistory()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].description, "5.0 + 3.0 = 8.0")

    def test_multiple_operations(self):
        self.calc.calculate(10, 5, '+')
        self.calc.calculate(10, 5, '-')
        self.calc.calculate(10, 5, '*')
        self.calc.calculate(10, 5, '/')
        history = self.calc.getHistory()
        self.assertEqual(len(history), 4)

    def test_invalid_input_handling(self):
        with self.assertRaises(InvalidInputError) as context:
            self.calc.calculate('a', 5, '+')
        self.assertTrue("could not convert string to float: 'a'" in str(context.exception))

if __name__ == "__main__":
    unittest.main()