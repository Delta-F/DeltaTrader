#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: comp_sharpe_ratio.py
@time: 2021/3/16 22:20
@desc:
'''
import data.stock as st
import strategy.base as stb
import pandas as pd
import matplotlib.pyplot as plt

# 获取3只股票的数据：比亚迪、宁德时代、隆基
codes = ['002594.XSHE', '300750.XSHE', '601012.XSHG']

# 容器：存放夏普
sharpes = []
for code in codes:
    data = st.get_single_price(code, 'daily', '2018-10-01', '2021-01-01')
    print(data.head())

    # 计算每只股票的夏普比率
    daily_sharpe, annual_sharpe = stb.calculate_sharpe(data)
    sharpes.append([code, annual_sharpe])  # 存放 [[c1,s1],[c2,s2]..]
    print(sharpes)

# 可视化3只股票并比较
sharpes = pd.DataFrame(sharpes, columns=['code', 'sharpe']).set_index('code')
print(sharpes)

# 绘制bar图
sharpes.plot.bar(title='Compare Annual Sharpe Ratio')
plt.xticks(rotation=30)
plt.show()
