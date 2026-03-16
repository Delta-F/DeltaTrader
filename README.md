<div align="center">

# DeltaTrader

[中文](README.md) | [English](README_en.md)

![version][version] ![py37][py37]

早期教程/演示项目：通过现成 Python 库演示量化全流程（数据 → 策略 → 回测 → 交易），偏入门与教学。生产级方案见下方 Delta 生态。

</div>

## 🎓 官方教程

- [慕课网 - 量化交易入门课程](https://coding.imooc.com/class/494.html)：本仓库配套入门课，用现成库走通数据、策略、回测与模拟交易，适合零基础上手。
- [慕课网 - 程序员 AI 量化理财体系课](https://class.imooc.com/sale/aiqwm)：进阶体系课，深度解析 deltafq 从 0 到 1 的架构设计，涵盖实盘闭环与工业级量化开发，学完入门后可继续进阶。

## 🚀 DeltaFQ AI 量化生态（进阶）

从研究、回测到实盘的一体化开源量化方案，轻量可扩展、适合个人与团队落地。

- [**deltafq**][deltafq]：纯原生手写量化框架，无重依赖，覆盖数据、策略、回测、实盘全链路。
- [**deltafstation**][deltafstation]：基于 deltafq 的量化交易云平台，集成数据服务、策略管理与交易接入，支持模拟与实盘。

## 📦 安装

```bash
git clone https://github.com/Delta-F/DeltaTrader.git
```

## ✨ 核心功能

- 📊 **行情数据** - 支持聚宽 JQData、财经网站爬虫
- ⚙️ **策略模型** - 基于简单规则创建交易策略
- 🤖 **自动交易** - 支持模拟实盘测试

## ⚡ 快速上手

获取股票价格数据：

```python
import data.stock as st

data = st.get_single_price(code='000001.XSHE',
                           time_freq='daily',
                           start_date='2021-01-01',
                           end_date='2021-02-01')
```

导出为 CSV：

```python
import data.stock as st

data = st.get_single_price(code='000001.XSHE')
st.export_data(data=data, filename='000001.XSHE', type='price')
```

## 🤝 参与贡献

- 反馈与改进：欢迎通过 [Issue][issue#1] 或邮件 leek_li@outlook.com 联系。
- 贡献者：[deltaf][deltaf]（框架设计及 Python 3 维护）、ACE（财经网站爬虫模块）。

## 📄 许可证

MIT License。

---

[version]: https://img.shields.io/badge/version-1.0-purpleviolet.svg
[py37]: https://img.shields.io/badge/python-3.7-red.svg
[deltaf]: https://github.com/Delta-F
[deltafq]: https://github.com/Delta-F/deltafq
[deltafstation]: https://github.com/Delta-F/deltafstation
[issue#1]: https://github.com/Delta-F/DeltaTrader/issues/1
