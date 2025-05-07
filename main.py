import argparse
from crawler.crawler_module import Crawler
from preprocessing.preprocess import Preprocessor
from analysis.analyzer import Analyzer
from visualization.visualization import Visualizer
import os

def check_file_exists(filepath, step_name):
    if not os.path.exists(filepath):
        print(f"❌ {step_name} 需要的文件未生成: {filepath}")
        return False
    return True

def run_pipeline(run_crawler, run_preprocess, run_analyze, run_visualize):
    try:
        if run_crawler:
            print("🚀 [1/4] 运行爬虫模块...")
            crawler = Crawler()
            crawler.run()
            print("✅ 爬虫模块完成")
            if not check_file_exists('data/rent_data.csv', '预处理模块'):
                return

        if run_preprocess:
            print("🧹 [2/4] 运行数据预处理模块...")
            preprocessor = Preprocessor()
            preprocessor.run()
            print("✅ 数据预处理完成")
            if not check_file_exists('data/cleaned_rent_data.csv', '分析模块'):
                return

        if run_analyze:
            print("📊 [3/4] 运行数据分析模块...")
            analyzer = Analyzer()
            analyzer.run()
            print("✅ 数据分析完成")
            if not check_file_exists('analysis_results.json', '可视化模块'):
                return

        if run_visualize:
            print("🎨 [4/4] 运行数据可视化模块...")
            visualizer = Visualizer()
            visualizer.run()
            print("✅ 可视化图表生成完成")

        print("🎉 全部任务已完成，请检查输出文件夹和日志文件。")

    except Exception as e:
        print(f"❌ 运行过程中出现错误: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="租房数据可视化系统")
    parser.add_argument('--crawler', action='store_true', help='运行爬虫模块')
    parser.add_argument('--preprocess', action='store_true', help='运行数据预处理模块')
    parser.add_argument('--analyze', action='store_true', help='运行数据分析模块')
    parser.add_argument('--visualize', action='store_true', help='运行数据可视化模块')
    parser.add_argument('--all', action='store_true', help='运行全流程')
    return parser.parse_args()

def main():
    print("✅ main.py 已启动")
    args = parse_arguments()
    run_pipeline(
        run_crawler=args.all or args.crawler,
        run_preprocess=args.all or args.preprocess,
        run_analyze=args.all or args.analyze,
        run_visualize=args.all or args.visualize
    )

if __name__ == '__main__':
    main()