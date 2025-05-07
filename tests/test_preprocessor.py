import unittest
import pandas as pd
from preprocessing.preprocess import Preprocessor

class TestPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = Preprocessor()
        data = {'Title': ['2室1厅', '3室2厅'],
                'Price': ['5000元/月', '8000元/月'],
                'Area': ['80㎡', '120㎡'],
                'Location': ['天河-员村', '越秀-东山口']}
        self.preprocessor.df = pd.DataFrame(data)

    def test_clean_price(self):
        self.preprocessor.clean_price()
        self.assertEqual(self.preprocessor.df['Price_num'].tolist(), [5000, 8000])

    def test_clean_area(self):
        self.preprocessor.clean_area()
        self.assertEqual(self.preprocessor.df['Area_num'].tolist(), [80.0, 120.0])

    def test_split_location(self):
        self.preprocessor.split_location()
        self.assertIn('Region', self.preprocessor.df.columns)
        self.assertIn('Street', self.preprocessor.df.columns)

    def test_safe_extract_none(self):
        result = self.preprocessor.safe_extract(r'\d+', None)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
