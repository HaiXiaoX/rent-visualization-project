import streamlit as st
import pandas as pd
import os
from crawler.crawler_module import Crawler
from preprocessing.preprocess import Preprocessor
from analysis.analyzer import Analyzer
from visualization.visualization import Visualizer

st.set_page_config(page_title="租房数据可视化系统", layout="wide")

st.title("🏠 租房数据可视化系统")

if st.button("运行爬虫"):
    crawler = Crawler()
    crawler.crawl()
    st.success("✅ 爬虫运行完成，数据已保存。")

if st.button("数据预处理"):
    preprocessor = Preprocessor()
    preprocessor.run()
    st.success("✅ 数据预处理完成。")

if st.button("数据分析"):
    analyzer = Analyzer()
    analyzer.run()
    st.success("✅ 数据分析完成。")

if st.button("生成可视化图表"):
    visualizer = Visualizer()
    visualizer.run()
    st.success("✅ 可视化图表已生成。")

st.header("查看数据")

data_file = "data/cleaned_rent_data.csv"
if os.path.exists(data_file):
    df = pd.read_csv(data_file)
    st.dataframe(df)

st.header("查看图表")

for img_file in ["basic_statistics.png", "region_group.png", "room_group.png"]:
    if os.path.exists(img_file):
        st.image(img_file, caption=img_file, use_column_width=True)
