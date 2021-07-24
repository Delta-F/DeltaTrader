# DeltaTrader

 ![py37][py37] ![version][version]

DeltaTrader，致力于打造一个极简好用的程序化交易框架，便于个人投资者优化自己的交易系统。

主要包含4大功能：获取行情数据（data）、创建交易策略（strategy）、计算评估指标并完成回测（backtest），以及模拟实盘交易（trader）的部分。
 
* 必看教程：https://coding.imooc.com/class/494.html
* 开源代码：https://github.com/Delta-F/DeltaTrader

## 合作招募

有意向重构or进行功能优化的，欢迎合作，微信：DeltaF_

## 简介

DeltaTrader是一个开源的量化交易接口，实现自动交易从未那么简单。

使用不到10行代码，你就可以获取任意A股数据，并实现自动化交易。

## 安装

可以通过clone该项目，实现引用。

## 简单入门实例

有了DeltaTrader，如果你想要获取股票数据，只需要这样：

```python
import data.stock as st

data = st.get_single_price(code='000001.XSHE',
                           time_freq='daily',
                           start_date='2021-01-01',
                           end_date='2021-02-01')
```

## 数据导出

将数据导出为.csv格式：

```python
import data.stock as st

data = st.get_single_price(code='000001.XSHE')

st.export_data(data=data, filename='000001.XSHE', type='price')
```

## 功能模块

- 行情数据：目前提供2中数据源获取方式（JQData数据接口、财经网站爬虫）
- 策略模型
- 自动化交易

## 参与作者

- [deltaf][deltaf]: 构架及维护Python3版本
- ACE：实时爬取财经网站股票行情数据

（待添加）

## 问题和建议

如果有什么问题或者建议都可以在[这里][issue#1]和我讨论

[version]: https://img.shields.io/badge/version-1.0-purpleviolet.svg
[py37]: https://img.shields.io/badge/python-3.7-red.svg
[deltaf]: https://github.com/Delta-F
[issue#1]: https://github.com/Delta-F/DeltaTrader/issues/1
