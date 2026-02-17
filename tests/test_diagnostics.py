import unittest
import pandas as pd
from src.diagnostics import check_missing_values, check_data_types, calculate_basic_metrics

class TestDiagnostics(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'a': [1, 2, None],
            'b': ['x', 'y', 'z'],
            'target': [0, 1, 0]
        })

    def test_check_missing_values(self):
        result = check_missing_values(self.df)
        self.assertEqual(result['a'], 1)
        self.assertEqual(result['b'], 0)

    def test_check_data_types(self):
        result = check_data_types(self.df)
        self.assertEqual(str(result['a']), 'float64')
        # Check if it's object or string, depending on pandas version
        dtype_str = str(result['b'])
        self.assertTrue(dtype_str == 'object' or 'string' in dtype_str.lower() or dtype_str == 'str')

    def test_calculate_basic_metrics(self):
        y_true = [0, 1, 0, 1]
        y_pred = [0, 1, 0, 0]
        metrics = calculate_basic_metrics(y_true, y_pred)
        self.assertEqual(metrics['accuracy'], 0.75)

if __name__ == '__main__':
    unittest.main()
