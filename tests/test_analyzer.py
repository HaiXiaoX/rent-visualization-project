import unittest
import pandas as pd
from analysis.analyzer import Analyzer

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = Analyzer()
        data = {
            'Price_num': [5000, 6000, 7000],
            'Area_num': [80, 90, 100],
            'Region': ['A', 'B', 'A'],
            'Rooms': ['2', '3', '2']
        }
        self.analyzer.df = pd.DataFrame(data)

    def test_basic_statistics(self):
        self.analyzer.basic_statistics()
        stats = self.analyzer.results.get('basic_statistics', {})
        self.assertIn('mean_price', stats)
        self.assertIn('mean_area', stats)

    def test_group_by_region(self):
        self.analyzer.group_by_region()
        region_group = self.analyzer.results.get('region_group', [])
        self.assertGreaterEqual(len(region_group), 1)

    def test_group_by_room_type(self):
        self.analyzer.group_by_room_type()
        room_group = self.analyzer.results.get('room_group', [])
        self.assertGreaterEqual(len(room_group), 1)

if __name__ == '__main__':
    unittest.main()
