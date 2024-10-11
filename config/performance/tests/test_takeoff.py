import unittest
import pandas as pd
from src.takeoff import compute_takeoff_ground_roll

performance_path = r'/config/performance/src/data'
takeoff_df = pd.read_csv(performance_path + '\\' + 'takeoff.csv')
roc_df = pd.read_csv(performance_path + '\\' + 'roc.csv', index_col=0)


class TestTakeoff(unittest.TestCase):

    def test_compute_takeoff_ground_roll(self):
        result1, result2 = compute_takeoff_ground_roll(2300, 0, 0, takeoff_df)
        obtained = (int(result1), int(result2))
        expected = (720, 1300)
        self.assertEqual(obtained, expected)


if __name__ == '__main__':
    unittest.main()
