#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: strategy.py
@time: 2021/3/5 19:18
@desc: 用来创建交易策略、生成交易信号
'''

import data.stock as st
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd


def compose_signal(data):
    """
    整合信号
    :param data:
    :return:
    """
    data['buy_signal'] = np.where((data['buy_signal'] == 1)
                                  & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1)
                                   & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data


def calculate_prof_pct(data):
    """
    计算单次收益率：开仓、平仓（开仓的全部股数）
    :param data:
    :return:
    """
    data = data[data['signal'] != 0]  # 筛选
    data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    data = data[data['signal'] == -1]
    return data


def calculate_cum_prof(data):
    """
    计算累计收益率
    :param data: dataframe
    :return:
    """
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data


def caculate_max_drawdown(data):
    """
    计算最大回撤比
    :param data:
    :return:
    """
    # 选取时间周期（时间窗口）
    window = 252
    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window=window, min_periods=1).max()
    # 计算当天的回撤比 = (谷值 — 峰值)/峰值 = 谷值/峰值 - 1
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大的回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window, min_periods=1).min()

    return data


def week_period_strategy(code, time_freq, start_date, end_date):
    """
    周期选股（周四买，周一卖）
    :param code:
    :param time_freq:
    :param start_date:
    :param end_date:
    :return:
    """
    data = st.get_single_price(code, time_freq, start_date, end_date)
    # 新建周期字段
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data['sell_signal'] = np.where((data['weekday'] == 0), -1, 0)

    data = compose_signal(data)  # 整合信号
    data = calculate_prof_pct(data)  # 计算收益
    data = calculate_cum_prof(data)  # 计算累计收益率
    # data = caculate_max_drawdown(data)  # 最大回撤
    return data


if __name__ == '__main__':
    # df = week_period_strategy('000001.XSHE', 'daily', None, datetime.date.today())
    # print(df[['close', 'signal', 'profit_pct', 'cum_profit']])
    # print(df.describe())
    # df['cum_profit'].plot()
    # plt.show()

    # 查看平安银行最大回撤
    df = st.get_single_price('000001.XSHE', 'daily', '2006-01-01', '2021-01-01')
    df = caculate_max_drawdown(df)
    print(df[['close', 'roll_max', 'daily_dd', 'max_dd']])
    df[['daily_dd', 'max_dd']].plot()
    plt.show()
