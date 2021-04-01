#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: ma_strategy.py
@time: 2021/3/23 15:54
@desc:双均线策略
'''
import data.stock as st
import strategy.base as strat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def ma_strategy(data, short_window=5, long_window=20):
    """
    双均线策略
    :param data: dataframe, 投资标的行情数据（必须包含收盘价）
    :param short_window: 短期n日移动平均线，默认5
    :param long_window: 长期n日移动平均线，默认20
    :return: 
    """
    data = pd.DataFrame(data)
    # 计算技术指标：ma短期、ma长期
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()

    # 生成信号：金叉买入、死叉卖出
    data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)

    # 过滤信号：st.compose_signal
    data = strat.compose_signal(data)

    # 计算单次收益
    data = strat.calculate_prof_pct(data)
    # print(data.describe())

    # 计算累计收益
    data = strat.calculate_cum_prof(data)

    # 数据预览
    # print(data[['close', 'short_ma', 'long_ma', 'buy_signal', 'sell_signal','signal']])

    # 删除多余的columns
    data.drop(labels=['buy_signal', 'sell_signal'], axis=1)

    return data


if __name__ == '__main__':
    # 股票列表
    stocks = ['000001.XSHE', '000858.XSHE', '002594.XSHE']
    # 存放累计收益率
    cum_profits = pd.DataFrame()
    # 循环获取数据
    for code in stocks:
        df = st.get_single_price(code, 'daily', '2016-01-01', '2021-01-01')
        df = ma_strategy(df)  # 调用双均线策略
        cum_profits[code] = df['cum_profit'].reset_index(drop=True)  # 存储累计收益率
        # 折线图
        df['cum_profit'].plot(label=code)
        # 筛选有信号点
        # df = df[df['signal'] != 0]
        # 预览数据
        print("开仓次数：", int(len(df)))
        # print(df[['close', 'signal', 'pro   、fit_pct', 'cum_profit']])

    # 预览
    print(cum_profits)
    # 可视化
    # cum_profits.plot()
    plt.legend()
    plt.title('Comparison of Ma Strategy Profits')
    plt.show()
