
# 🏠 深圳租房数据可视化系统

本项目基于 Python 实现了一个深圳地区租房数据采集与可视化分析系统，涵盖了数据爬虫、预处理、统计分析与交互式图表展示等完整流程。生成结果为一个图表导航 HTML 页面，支持交互式数据浏览，适用于房产数据分析、教学示例或毕业设计展示。

## 📁 项目结构

```
rent_visualization_project/
├── crawler/               # 爬虫模块（采集租房数据）
│   └── crawler_module.py
├── preprocessing/         # 数据预处理模块（清洗与字段提取）
│   └── preprocess.py
├── analysis/              # 数据分析模块（统计与分组）
│   └── analyzer.py
├── visualization/         # 可视化模块（生成图表与汇总页）
│   └── visualization.py
├── data/                  # 存放原始与清洗后的数据
│   ├── rent_data.csv
│   └── cleaned_rent_data.csv
├── output/                # 图表输出目录
│   ├── basic_statistics.html
│   ├── report.html        # 图表汇总页面
│   └── ...（其他图表）
├── config.json            # 模块配置文件
├── main.py                # 项目主入口
└── requirements.txt       # 项目依赖
```

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

如果你在中国大陆，建议换源安装依赖：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2️⃣ 执行主程序

**一键运行完整流程：**

```bash
python main.py --all
```

**按模块分开运行：**

```bash
python main.py --crawler       # 仅运行爬虫模块
python main.py --preprocess    # 仅运行数据预处理
python main.py --analyze       # 仅运行数据分析
python main.py --visualize     # 仅运行数据可视化
```

## 📊 可视化图表示例

运行后，所有图表将保存在 `output/` 文件夹中。你可以直接双击 `output/report.html` 浏览所有交互式图表，包括：

- 区域房源分布（饼图）
- 房型分布（饼图）
- 区域平均租金（柱状图）
- 房型平均租金（柱状图）
- 面积 vs 租金（散点图）
- 每平米租金分布（柱状图）
- 各房型面积箱线图
- 基础统计柱状图

## ⚙️ 配置说明（可选）

项目参数通过 `config.json` 管理，例如：

```json
{
  "analyzer": {
    "input_file": "data/cleaned_rent_data.csv",
    "output_file": "analysis_results.json"
  },
  "preprocess": {
    "input_file": "data/rent_data.csv",
    "output_file": "data/cleaned_rent_data.csv"
  },
  "visualization": {
    "output_folder": "output"
  }
}
```

## 🧩 依赖环境（requirements.txt）

- pandas
- numpy
- plotly
- argparse
- logging

## 🌟 项目特色

- ✅ 全流程自动化：从爬虫到报告输出一键搞定
- ✅ 交互式图表：基于 Plotly，美观又实用
- ✅ 中文标签：所有图表/字段/标题全面中文化
- ✅ 页面美观：汇总页面清晰排版，支持导航跳转
- ✅ 日志记录：每个模块独立记录日志，便于调试

## 📌 TODO 可扩展方向

- [ ] 加入地理位置地图标记（可用高德/百度地图 API）
- [ ] 增加价格趋势对比（同比、环比分析）
- [ ] 加入 Web 部署（Flask/Django）
- [ ] 房源筛选与关键词搜索功能
- [ ] 导出 PDF 报告、图片等格式

## 👨‍💻 作者信息

> **Xander**  
> 2025 年毕业设计项目  
> 🚫 本项目仅供学习交流，禁止用于商业用途  
> 欢迎 star、fork、issue 一起完善！
