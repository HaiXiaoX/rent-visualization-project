import pandas as pd
import json
import numpy as np
import logging
import os
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


class Analyzer:
    def __init__(self, config_file: str = "config.json"):
        # 默认路径
        self.config_file = config_file
        self.input_file = "data/cleaned_rent_data.csv"
        self.output_json = "analysis_results.json"
        self.df = pd.DataFrame()
        self.results: dict = {}

        # 读取配置文件
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                cfg = json.load(f).get("analyzer", {})
                self.input_file = cfg.get("input_file", self.input_file)
                self.output_json = cfg.get("output_file", self.output_json)

        # 确保 log 目录存在
        if not os.path.exists("log"):
            os.makedirs("log")

        # 日志
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("log/analyzer.log", encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )

    # ---------- 数据加载 ----------
    def load_data(self):
        if not os.path.exists(self.input_file):
            logging.error(f"❌ 找不到输入文件: {self.input_file}")
            return
        try:
            self.df = pd.read_csv(self.input_file, encoding="utf-8-sig")
            logging.info(f"加载数据成功，共 {len(self.df)} 行")
        except Exception as e:
            logging.error(f"加载数据失败: {e}")
            self.df = pd.DataFrame()

    # ---------- 统计 ----------
    def basic_statistics(self):
        if not {"Price_num", "Area_num"}.issubset(self.df.columns):
            logging.warning("缺少 Price_num 或 Area_num，跳过基本统计")
            return
        self.results["basic_statistics"] = {
            "mean_price": self.df["Price_num"].mean(),
            "max_price": self.df["Price_num"].max(),
            "min_price": self.df["Price_num"].min(),
            "mean_area": self.df["Area_num"].mean(),
            "max_area": self.df["Area_num"].max(),
            "min_area": self.df["Area_num"].min(),
        }
        logging.info("完成基本统计分析")

    def group_by_region(self):
        if "Region" not in self.df.columns:
            logging.warning("Region 列不存在，跳过区域分组")
            return
        df_valid = self.df[self.df["Region"] != "未知区域"]
        group = (
            df_valid.groupby("Region")["Price_num"]
            .agg(["count", "mean", "max", "min"])
            .round(2)
            .reset_index()
        )
        self.results["region_group"] = group.to_dict(orient="records")
        logging.info("完成按区域分组")


    def group_by_room_type(self):
        if "Rooms" not in self.df.columns:
            logging.warning("Rooms 列不存在，跳过房型分组")
            return
        df_valid = self.df[self.df["Rooms"] != "未提取"]
        group = (
            df_valid.groupby("Rooms")["Price_num"]
            .agg(["count", "mean", "max", "min"])
            .round(2)
            .reset_index()
        )
        self.results["room_group"] = group.to_dict(orient="records")
        logging.info("完成按房型分组")


    # ---------- 保存 ----------
    def _json_converter(self, obj):
        if isinstance(obj, np.generic):
            return obj.item()
        raise TypeError(f"{type(obj)} 不能序列化为 JSON")

    def save_results(self):
        try:
            with open(self.output_json, "w", encoding="utf-8") as f:
                json.dump(
                    self.results,
                    f,
                    ensure_ascii=False,
                    indent=4,
                    default=self._json_converter,
                )
            logging.info(f"分析结果已保存 → {self.output_json}")
        except Exception as e:
            logging.error(f"保存分析结果失败: {e}")

    # ---------- 主流程 ----------
    def run(self):
        self.load_data()
        if self.df.empty:
            logging.error("数据为空，终止分析")
            return
        self.basic_statistics()
        self.group_by_region()
        self.group_by_room_type()
        self.save_results()
