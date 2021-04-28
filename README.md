# DeltaTrader

 ![py37][py37] ![version][version]

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

## 作以及者

- [deltaf][deltaf]: 构架及维护Python3版本
- ACE：实时爬取财经网站股票行情数据

（待添加）

## 问题和建议

如果有什么问题或者建议都可以在[这里][issue#1]和我讨论

[version]: https://img.shields.io/badge/version-1.0-purpleviolet.svg
[py37]: https://img.shields.io/badge/python-3.7-red.svg
[deltaf]: https://github.com/Delta-F
[issue#1]: https://github.com/Delta-F/DeltaTrader/issues/1
