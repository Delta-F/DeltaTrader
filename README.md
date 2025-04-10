<div align="right">

[English](#delta-trader) | [中文](#delta-trader-中文说明)

</div>

# DeltaTrader

![py37][py37] ![version][version]

DeltaTrader is a minimalist, user-friendly framework for algorithmic trading, designed to help individual investors optimize their trading systems.

It focuses on four core modules: retrieving market data (`data`), creating trading strategies (`strategy`), performing backtests with evaluation metrics (`backtest`), and executing simulated live trades (`trader`).

- 🎓 Tutorial: https://coding.imooc.com/class/494.html
- 📂 Source Code: https://github.com/Delta-F/DeltaTrader

## 🤝 Collaboration

Interested in refactoring or enhancing features? Let’s collaborate: leek_li@outlook.com

## 📌 Overview

DeltaTrader is an open-source interface for quantitative trading. Automated trading has never been so easy.

With fewer than 10 lines of code, you can retrieve A-share stock data and execute automated strategies.

## 🚀 Installation

Clone the repository to get started:

```bash
git clone https://github.com/Delta-F/DeltaTrader.git
```

## ⚡ Quick Start

Retrieve stock price data with:

```python
import data.stock as st

data = st.get_single_price(code='000001.XSHE',
                           time_freq='daily',
                           start_date='2021-01-01',
                           end_date='2021-02-01')
```

## 💾 Export Data

Export the data as a CSV file:

```python
import data.stock as st

data = st.get_single_price(code='000001.XSHE')

st.export_data(data=data, filename='000001.XSHE', type='price')
```

## 🧩 Core Modules

- 📊 **Market Data**: Supports two sources (JQData API and web scraping)
- ⚙️ **Strategy Models**: Create strategies based on simple logic
- 🤖 **Automated Trading**: Supports simulated live trading

## 👨‍💻 Contributors

- [deltaf][deltaf]: Framework architect and Python 3 maintainer
- ACE: Market data crawler for financial websites

(More contributors welcome!)

## 💡 Issues & Feedback

If you have any issues or suggestions, feel free to open a discussion on the [Issues page][issue#1].

---

<div align="right">

[English](#delta-trader) | [中文](#delta-trader-中文说明)

</div>

---

# DeltaTrader 中文说明

![py37][py37] ![version][version]

DeltaTrader，致力于打造一个极简好用的程序化交易框架，便于个人投资者优化自己的交易系统。

主要包含 4 大核心模块：行情数据（data）、交易策略（strategy）、回测（backtest）、以及模拟实盘交易（trader）。

- 🎓 教程入口：https://coding.imooc.com/class/494.html
- 📂 开源代码：https://github.com/Delta-F/DeltaTrader

## 🤝 合作招募

如果你对重构本项目或添加新功能有兴趣，欢迎联系我：leek_li@outlook.com

## 📌 项目简介

DeltaTrader 是一个开源的量化交易接口，实现自动交易从未如此简单。

不到 10 行代码，你就可以获取任意 A 股数据，并实现自动化交易。

## 🚀 安装方式

直接 clone 项目代码即可使用：

```bash
git clone https://github.com/Delta-F/DeltaTrader.git
```

## ⚡ 快速开始

获取股票价格数据：

```python
import data.stock as st

data = st.get_single_price(code='000001.XSHE',
                           time_freq='daily',
                           start_date='2021-01-01',
                           end_date='2021-02-01')
```

## 💾 数据导出

将数据导出为 CSV 文件：

```python
import data.stock as st

data = st.get_single_price(code='000001.XSHE')

st.export_data(data=data, filename='000001.XSHE', type='price')
```

## 🧩 功能模块

- 📊 **行情数据**：支持两个数据源（聚宽 JQData、财经网站爬虫）
- ⚙️ **策略模型**：基于简单的规则创建交易策略
- 🤖 **自动交易**：支持模拟实盘测试

## 👨‍💻 作者

- [deltaf][deltaf]：框架设计及 Python 3 版本维护
- ACE：财经网站行情爬虫模块

（欢迎补充更多贡献者）

## 💡 问题与建议

如果你在使用中遇到问题或有建议，欢迎通过 [Issues 区][issue#1] 交流反馈。

---

<div align="right">

[English](#delta-trader) | [中文](#delta-trader-中文说明)

</div>

[version]: https://img.shields.io/badge/version-1.0-purpleviolet.svg
[py37]: https://img.shields.io/badge/python-3.7-red.svg
[deltaf]: https://github.com/Delta-F
[issue#1]: https://github.com/Delta-F/DeltaTrader/issues/1
