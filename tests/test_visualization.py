import unittest
import os
from visualization.visualization import Visualizer

class TestVisualizer(unittest.TestCase):
    def setUp(self):
        # 构造一个简单的分析结果 JSON 文件
        self.json_file = 'test_analysis_results.json'
        sample_data = {
            "basic_statistics": {"mean_price": 6000, "max_price": 7000, "min_price": 5000, "mean_area": 90, "max_area": 100, "min_area": 80},
            "region_group": [{"Region": "A", "count": 2, "mean": 6000, "max": 7000, "min": 5000}],
            "room_group": [{"Rooms": "2", "count": 2, "mean": 6000, "max": 7000, "min": 5000}]
        }
        import json
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=4)

        self.visualizer = Visualizer(json_file=self.json_file)

    def test_load_results(self):
        self.visualizer.load_results()
        self.assertIn('basic_statistics', self.visualizer.results)

    def test_plot_basic_statistics(self):
        self.visualizer.load_results()
        self.visualizer.plot_basic_statistics()
        self.assertTrue(os.path.exists('basic_statistics.png'))

    def test_plot_region_group(self):
        self.visualizer.load_results()
        self.visualizer.plot_region_group()
        self.assertTrue(os.path.exists('region_group.png'))

    def test_plot_room_group(self):
        self.visualizer.load_results()
        self.visualizer.plot_room_group()
        self.assertTrue(os.path.exists('room_group.png'))

    def tearDown(self):
        # 清理测试文件
        os.remove(self.json_file)
        for file in ['basic_statistics.png', 'region_group.png', 'room_group.png']:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    unittest.main()
