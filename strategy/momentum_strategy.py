#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: momentum_strategy.py
@time: 2021/4/14 23:35
@desc: 动量策略（正向）
'''
import data.stock as st
import pandas as pd
import numpy as np
import strategy.base as base
import matplotlib.pyplot as plt


def get_data(start_date, end_date, use_cols, index_symbol='000300.XSHG'):
    """
    获取股票收盘价数据，并拼接为一个df
    :param start_date: str
    :param end_date: str
    :param use_cols: list
    :param index_symbol: str
    :return data_concat: df，拼接后的数据表
    """
    # 获取股票列表代码：沪深300持有个股、创业板、上证
    stocks = st.get_index_list(index_symbol)
    # 拼接收盘价数据
    data_concat = pd.DataFrame()
    # 获取股票数据
    for code in stocks:
        data = st.get_csv_price(code, start_date, end_date, use_cols)
        # 拼接多个股票的收盘价：日期 股票A收盘价 股票B收盘价 ...
        data.columns = [code]
        data_concat = pd.concat([data_concat, data], axis=1)
    # 预览股票数据
    # print(data_concat.tail())
    return data_concat


def momentum(data_concat, shift_n=1, top_n=4):
    """

    :param data_concat: df
    :param shift_n: int,表示业绩统计周期（单位：月）
    :return:
    """
    # 转换时间频率：日->月
    data_concat.index = pd.to_datetime(data_concat.index)
    data_month = data_concat.resample('M').last()
    # 计算过去N个月的收益率 = 期末值/期初值 - 1 =（期末-期初）/ 期初
    # optional：对数收益率 = log（期末值 / 期初值）
    shift_return = data_month / data_month.shift(shift_n) - 1
    print(shift_return.head())
    # print(shift_return.shift(-1))

    # 生成交易信号：收益率排前n的>赢家组合>买入1，排最后n个>输家>卖出-1
    buy_signal = get_top_stocks(shift_return, top_n)
    sell_signal = get_top_stocks(-1 * shift_return, top_n)
    signal = buy_signal - sell_signal
    print(signal.head())

    # 计算投资组合收益率
    returns = base.caculate_portfolio_return(shift_return, signal, top_n * 2)
    print(returns.head())

    # 评估策略效果：总收益率、年化收益率、最大回撤、夏普比
    returns = base.evaluate_strategy(returns)

    # 数据预览
    # print(data_month.head())
    return returns


def get_top_stocks(data, top_n):
    """
    找到前n位的极值，并转换为信号返回
    :param data: df
    :param top_n: int, 表示要产生信号的个数
    :return signals: df, 返回0-1信号数据表
    """
    # 初始化信号容器
    signals = pd.DataFrame(index=data.index, columns=data.columns)
    # 对data的每一行进行遍历，找里面的最大值，并利用bool函数标注0或1信号
    for index, row in data.iterrows():
        signals.loc[index] = row.isin(row.nlargest(top_n)).astype(np.int)
    return signals


if __name__ == '__main__':
    # 测试：获取沪深300个股数据
    data = get_data('2016-01-01', '2021-04-04', ['date', 'close'])
    # 测试：动量策略
    returns = momentum(data)
    # 存储结果
    returns.to_csv('/Users/ztnn/PycharmProjects/DeltaTrader/strategy/results/momentum.csv')
    # 可视化每个月的收益率
    # returns['cum_profit'].plot()
    # plt.show()
