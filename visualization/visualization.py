import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging

from typing import Callable


class Visualizer:
    def __init__(self, config_file='config.json', json_file='analysis_results.json'):
        self.config_file = config_file
        self.json_file = json_file
        self.output_folder = 'output'
        self.results = {}

        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                viz_cfg = config.get('visualization', {})
                self.output_folder = viz_cfg.get('output_folder', 'output')

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        if not os.path.exists('log'):
            os.makedirs('log')

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s [%(levelname)s] %(message)s',
                            handlers=[
                                logging.FileHandler("log/visualizer.log", encoding='utf-8'),
                                logging.StreamHandler()
                            ])

    def load_results(self):
        if not os.path.exists(self.json_file):
            logging.error(f"❌ 找不到分析结果文件: {self.json_file}")
            return False
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.results = json.load(f)
            logging.info(f"✅ 加载分析结果成功: {self.json_file}")
            return True
        except Exception as e:
            logging.error(f"加载分析结果失败: {e}")
            return False

    def save_html(self, fig, name):
        filepath = os.path.join(self.output_folder, f'{name}.html')
        fig.write_html(filepath)
        logging.info(f"✅ 图表已保存: {filepath}")

    def plot_basic_statistics(self):
        stats = self.results.get('basic_statistics', {})
        if not stats:
            logging.warning("⚠️ 无 basic_statistics 数据")
            return
        cn_labels = {
            "mean_price": "平均价格",
            "max_price": "最高价格",
            "min_price": "最低价格",
            "mean_area": "平均面积",
            "max_area": "最大面积",
            "min_area": "最小面积"
        }
        keys = list(stats.keys())
        values = list(stats.values())
        labels = [cn_labels.get(k, k) for k in keys]

        fig = px.bar(x=labels, y=values, title='基础统计指标')
        fig.update_layout(xaxis_title='', yaxis_title='数值')
        self.save_html(fig, 'basic_statistics')

    def plot_region_group(self):
        df = pd.DataFrame(self.results.get('region_group', []))
        if df.empty:
            logging.warning("⚠️ 无 region_group 数据")
            return
        fig = px.bar(df, x='Region', y='mean', title='各区域平均租金',
                     labels={'Region': '区域', 'mean': '平均租金（元）'}, text_auto=True)
        fig.update_traces(hovertemplate='区域: %{x}<br>平均租金: %{y} 元')
        fig.update_layout(xaxis_title='区域', yaxis_title='平均租金（元）')
        self.save_html(fig, 'region_group')

    def plot_room_group(self):
        df = pd.DataFrame(self.results.get('room_group', []))
        if df.empty:
            logging.warning("⚠️ 无 room_group 数据")
            return
        fig = px.bar(df, x='Rooms', y='mean', title='各房型平均租金',
                     labels={'Rooms': '房型', 'mean': '平均租金（元）'}, text_auto=True)
        fig.update_traces(hovertemplate='房型: %{x}<br>平均租金: %{y} 元')
        fig.update_layout(xaxis_title='房型', yaxis_title='平均租金（元）')
        self.save_html(fig, 'room_group')

    def plot_region_distribution(self):
        df = pd.read_csv("data/cleaned_rent_data.csv")
        if "Region" not in df:
            return
        counts = df['Region'].value_counts().reset_index()
        counts.columns = ['Region', 'Count']
        fig = px.pie(counts, names='Region', values='Count', title='区域房源分布',
                     labels={'Region': '区域', 'Count': '房源数量'})
        self.save_html(fig, 'region_distribution')

    def plot_room_distribution(self):
        df = pd.read_csv("data/cleaned_rent_data.csv")
        if "Rooms" not in df:
            return
        counts = df['Rooms'].value_counts().reset_index()
        counts.columns = ['Rooms', 'Count']
        fig = px.pie(counts, names='Rooms', values='Count', title='房型分布',
                     labels={'Rooms': '房型', 'Count': '房源数量'})
        self.save_html(fig, 'room_distribution')

    def plot_price_vs_area(self):
        df = pd.read_csv("data/cleaned_rent_data.csv")
        fig = px.scatter(df, x='Area_num', y='Price_num', color='Region',
                         title='面积与价格关系',
                         labels={'Area_num': '面积（㎡）', 'Price_num': '租金（元）', 'Region': '区域', 'Location': '地址'},
                         hover_data=['Location'])
        self.save_html(fig, 'price_vs_area')

    def plot_price_distribution(self):
        df = pd.read_csv("data/cleaned_rent_data.csv")
        fig = px.histogram(
            df,
            x='Price_num',
            nbins=30,
            title='租金分布',
            labels={'Price_num': '租金（元）'},
            opacity=0.75,
            color_discrete_sequence=["#636EFA"]
        )
        fig.update_layout(
            xaxis_title="租金（元）",
            yaxis_title="房源数量",
            bargap=0.1,
            plot_bgcolor="#F7FAFF",
            paper_bgcolor="#F7FAFF",
            font=dict(size=14)
        )
        self.save_html(fig, 'price_distribution')


    def plot_unit_price_distribution(self):
        df = pd.read_csv("data/cleaned_rent_data.csv")
        if 'Price_num' in df.columns and 'Area_num' in df.columns:
            df['UnitPrice'] = df['Price_num'] / df['Area_num']
        else:
            logging.warning("⚠️ 缺少价格或面积列，无法计算单位租金")
            return
        df = df[(df["UnitPrice"] > 20) & (df["UnitPrice"] < 200)]

        fig = px.histogram(
            df,
            x="UnitPrice",
            nbins=30,
            title="每平米租金分布（单位：元/㎡）",
            labels={"UnitPrice": "单位租金（元/㎡）"},
            opacity=0.75,
            color_discrete_sequence=["#636EFA"]
        )

        fig.update_layout(
            xaxis_title="单位租金（元/㎡）",
            yaxis_title="房源数量",
            bargap=0.05,
            plot_bgcolor="#F7FAFF",
            paper_bgcolor="#F7FAFF",
            font=dict(size=14)
        )

        self.save_html(fig, "unit_price_distribution")

    def plot_area_box_by_room(self):
        import pandas as pd
        import plotly.graph_objects as go

        df = pd.read_csv("data/cleaned_rent_data.csv")

        fig = go.Figure()

        room_types = df['Rooms'].unique()

        for room in room_types:
            subset = df[df['Rooms'] == room]['Area_num']
            fig.add_trace(
                go.Box(
                    y=subset,
                    name=room,
                    boxpoints='outliers',
                    jitter=0.3,
                    pointpos=-1.8,
                    marker_color='rgb(93, 164, 214)',
                    line_color='rgb(93, 164, 214)',
                    hovertemplate=(
                        f"房型：{room}<br>" +
                        "最小值：%{y}<br>" +
                        "最大值：%{y}<br>" +
                        "中位数：%{y}<br>" +
                        "上四分位数：%{y}<br>" +
                        "下四分位数：%{y}<extra></extra>"
                    )
                )
            )

        fig.update_layout(
            title="各房型面积箱线图",
            xaxis_title="房型",
            yaxis_title="面积（㎡）",
            font=dict(size=16),
            plot_bgcolor="#F7FAFF",
            paper_bgcolor="#F7FAFF"
        )

        self.save_html(fig, "area_box_by_room")
    
    def generate_summary_html(self):
        html = f"""
        <!DOCTYPE html>
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <title>租房数据可视化报告</title>
            <style>
                body {{
                    font-family: "微软雅黑", sans-serif;
                    background-color: #f2f4f8;
                    padding: 30px;
                    margin: 0;
                }}
                h1 {{
                    text-align: center;
                    color: #1a1a1a;
                    margin-bottom: 30px;
                }}
                .grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
                    gap: 30px;
                    max-width: 1600px;
                    margin: auto;
                }}
                .card {{
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
                }}
                iframe {{
                    width: 100%;
                    height: 500px;
                    border: none;
                    border-radius: 6px;
                }}
                h2 {{
                    font-size: 20px;
                    margin-bottom: 10px;
                    color: #444;
                    text-align: center;
                }}
                nav {{
                    text-align: center;
                    margin-bottom: 40px;
                }}
                nav a {{
                    margin: 0 15px;
                    text-decoration: none;
                    color: #0077cc;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>

        <h1>🏘️ 深圳租房数据可视化报告</h1>

        <nav>
            <a href="#basic">基础统计</a>
            <a href="#region">区域分析</a>
            <a href="#room">房型分析</a>
            <a href="#price">价格分布</a>
            <a href="#unit">单位租金</a>
        </nav>

        <div class="grid" id="basic">
            <div class="card">
                <h2>基础统计</h2>
                <iframe src="basic_statistics.html"></iframe>
            </div>
        </div>

        <div class="grid" id="region">
            <div class="card">
                <h2>区域分布</h2>
                <iframe src="region_distribution.html"></iframe>
            </div>
            <div class="card">
                <h2>区域平均租金</h2>
                <iframe src="region_group.html"></iframe>
            </div>
        </div>

        <div class="grid" id="room">
            <div class="card">
                <h2>房型分布</h2>
                <iframe src="room_distribution.html"></iframe>
            </div>
            <div class="card">
                <h2>房型平均租金</h2>
                <iframe src="room_group.html"></iframe>
            </div>
            <div class="card">
                <h2>房型面积箱线图</h2>
                <iframe src="area_box_by_room.html"></iframe>
            </div>
        </div>

        <div class="grid" id="price">
            <div class="card">
                <h2>租金 vs 面积</h2>
                <iframe src="price_vs_area.html"></iframe>
            </div>
            <div class="card">
                <h2>租金分布</h2>
                <iframe src="price_distribution.html"></iframe>
            </div>
        </div>

        <div class="grid" id="unit">
            <div class="card">
                <h2>每平米租金分布</h2>
                <iframe src="unit_price_distribution.html"></iframe>
            </div>
        </div>

        </body>
        </html>
        """
        with open(os.path.join(self.output_folder, "report.html"), "w", encoding="utf-8") as f:
            f.write(html)
        logging.info("✅ 汇总图表页面（美化版）已生成 → report.html")




    def run(self):
        if not self.load_results():
            logging.error("终止可视化生成")
            return

        self.plot_basic_statistics()
        self.plot_region_group()
        self.plot_room_group()
        self.plot_region_distribution()
        self.plot_room_distribution()
        self.plot_price_vs_area()
        self.plot_price_distribution()
        self.plot_unit_price_distribution()
        self.plot_area_box_by_room()
        self.generate_summary_html()
