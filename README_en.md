<div align="center">

# DeltaTrader

[中文](README.md) | [English](README_en.md)

![version][version] ![py37][py37]

Early tutorial/demo project: walks through the full quantitative workflow with off-the-shelf Python libraries (data → strategy → backtest → trader). For production use, see the Delta ecosystem below.

</div>

## 🎓 Official Tutorial

- [imooc - Intro to Quantitative Trading](https://coding.imooc.com/class/494.html): Companion course for this repo; data, strategy, backtest, and simulated trading with existing libraries. Suitable for beginners.
- [imooc - Programmer's AI Quantitative Finance System Course](https://class.imooc.com/sale/aiqwm): Advanced course; deep dive into deltafq architecture from 0 to 1, live trading loop, and production-grade quant development. For those who have finished the intro course.

## 🚀 DeltaFQ AI Quant Ecosystem (Next Step)

Open-source quant stack from research and backtest to live trading; lightweight, extensible, for individuals and teams.

- [**deltafq**][deltafq]: Pure native quant framework, minimal dependencies, full pipeline from data, strategy, backtest to live.
- [**deltafstation**][deltafstation]: Quant trading platform built on deltafq; data services, strategy management, and trading connectivity, with sim and live support.

## 📦 Installation

```bash
git clone https://github.com/Delta-F/DeltaTrader.git
```

## ✨ Core Features

- 📊 **Market Data** - JQData API and web scraping
- ⚙️ **Strategy Models** - Rule-based strategy creation
- 🤖 **Automated Trading** - Simulated live trading

## ⚡ Quick Start

Get stock price data:

```python
import data.stock as st

data = st.get_single_price(code='000001.XSHE',
                           time_freq='daily',
                           start_date='2021-01-01',
                           end_date='2021-02-01')
```

Export to CSV:

```python
import data.stock as st

data = st.get_single_price(code='000001.XSHE')
st.export_data(data=data, filename='000001.XSHE', type='price')
```

## 🤝 Contributing

- Feedback and improvements: [Issue][issue#1] or leek_li@outlook.com.
- Contributors: [deltaf][deltaf] (framework design & Python 3), ACE (market data crawler).

## 📄 License

MIT License.

---

[version]: https://img.shields.io/badge/version-1.0-purpleviolet.svg
[py37]: https://img.shields.io/badge/python-3.7-red.svg
[deltaf]: https://github.com/Delta-F
[deltafq]: https://github.com/Delta-F/deltafq
[deltafstation]: https://github.com/Delta-F/deltafstation
[issue#1]: https://github.com/Delta-F/DeltaTrader/issues/1
