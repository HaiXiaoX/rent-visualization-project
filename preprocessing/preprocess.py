import pandas as pd
import json
import logging
import os
import warnings
import re

# 忽略 pandas 的 FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

class Preprocessor:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.input_file = 'data/rent_data.csv'
        self.output_file = 'data/cleaned_rent_data.csv'
        self.df = pd.DataFrame()

        # 读取 config.json 中的路径设置
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                preprocess_cfg = config.get('preprocess', {})
                self.input_file = preprocess_cfg.get('input_file', self.input_file)
                self.output_file = preprocess_cfg.get('output_file', self.output_file)

        # 确保 log 文件夹存在
        if not os.path.exists('log'):
            os.makedirs('log')

        # 日志配置（控制台 + 文件）
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s [%(levelname)s] %(message)s',
                            handlers=[
                                logging.FileHandler("log/preprocessor.log", encoding='utf-8'),
                                logging.StreamHandler()
                            ])

    def load_data(self):
        if not os.path.exists(self.input_file):
            logging.error(f"❌ 找不到输入文件: {self.input_file}")
            self.df = pd.DataFrame()
            return
        try:
            self.df = pd.read_csv(self.input_file, encoding='utf-8-sig')
            logging.info(f"加载数据成功，共 {len(self.df)} 行")
        except Exception as e:
            logging.error(f"加载数据失败: {e}")
            self.df = pd.DataFrame()

    def clean_data(self):
        if self.df.empty:
            logging.error("数据为空，无法清理")
            return

        # 原功能：去重 + 提取价格/面积 + 清洗地址
        self.df.drop_duplicates(inplace=True)

        self.df['Price_num'] = pd.to_numeric(
            self.df['Price'].astype(str).str.extract(r'(\d+\.?\d*)')[0],
            errors='coerce'
        )
        self.df['Area_num'] = pd.to_numeric(
            self.df['Area'].astype(str).str.extract(r'(\d+\.?\d*)')[0],
            errors='coerce'
        )

        self.df['Location'] = self.df['Location'].fillna('未提供住址')
        self.df.loc[self.df['Location'].isin(['', 'N/A']), 'Location'] = '未提供住址'

        # 新增拓展：提取 Region 和 Rooms 字段（不影响原始流程）
        if 'Region' not in self.df:
            self.df['Region'] = self.df['Location'].apply(
                lambda x: x.split(' - ')[0] if isinstance(x, str) and ' - ' in x else '未知区域')

        if 'Rooms' not in self.df:
            self.df['Rooms'] = self.df['Title'].apply(
                lambda x: re.search(r'(\d+室\d+厅)', x).group(1) if isinstance(x, str) and re.search(r'(\d+室\d+厅)', x) else '未提取')

        # 添加单位租金列
        self.df['UnitPrice'] = self.df['Price_num'] / self.df['Area_num']

        self.df.dropna(subset=['Price_num', 'Area_num', 'UnitPrice'], inplace=True)

        try:
            self.df.to_csv(self.output_file, index=False, encoding='utf-8-sig')
            logging.info(f"数据清理完成并保存，共 {len(self.df)} 行 → {self.output_file}")
        except Exception as e:
            logging.error(f"保存数据失败: {e}")

    def run(self):
        self.load_data()
        if self.df.empty:
            logging.error("数据为空，退出预处理")
            return
        self.clean_data()
        