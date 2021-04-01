#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: week_strategy.py
@time: 2021/3/5 19:18
@desc: 周期性交易策略
'''
import data.stock as st
import numpy as np
import datetime
import strategy.base as base
import matplotlib.pyplot as plt


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

    data = base.compose_signal(data)  # 整合信号
    data = base.calculate_prof_pct(data)  # 计算收益
    # data = base.calculate_cum_prof(data)  # 计算累计收益率
    # data = base.caculate_max_drawdown(data)  # 最大回撤
    return data


if __name__ == '__main__':
    df = week_period_strategy('000001.XSHE', 'daily', None, datetime.date.today())
    print(df[['close', 'signal', 'profit_pct']])
    print(df[['close', 'signal', 'profit_pct']].describe())
    # df['profit_pct'].plot()
    # plt.hist(df['profit_pct'], bins=30)
    # plt.show()

    # 查看平安银行最大回撤
    # df = st.get_single_price('000001.XSHE', 'daily', '2006-01-01', '2021-01-01')
    # df = caculate_max_drawdown(df)
    # print(df[['close', 'roll_max', 'daily_dd', 'max_dd']])
    # df[['daily_dd', 'max_dd']].plot()
    # plt.show()

    # 计算夏普比率
    # df = st.get_single_price('000001.XSHE', 'daily', '2006-01-01', '2021-01-01')
    # sharpe = calculate_sharpe(df)
    # print(sharpe)
