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


def evaluate_strategy(data):
    """
    评估策略收益表现
    :param data: dataframe, 包含单次收益率数据
    :return results: dict, 评估指标数据
    """
    # 评估策略效果：总收益率、年化收益率、最大回撤、夏普比
    data = calculate_cum_prof(data)

    # 获取总收益率
    total_return = data['cum_profit'].iloc[-1]
    # 计算年化收益率（每月开仓）
    annual_return = data['profit_pct'].mean() * 12

    # 计算近一年最大回撤
    data = caculate_max_drawdown(data, window=12)
    # print(data)
    # 获取近一年最大回撤
    max_drawdown = data['max_dd'].iloc[-1]

    # 计算夏普比率
    sharpe, annual_sharpe = calculate_sharpe(data)

    # 放到dict中
    results = {'总收益率': total_return, '年化收益率': annual_return,
               '最大回撤': max_drawdown, '夏普比率': annual_sharpe}

    # 打印评估指标
    for key, value in results.items():
        print(key, value)

    return data


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
    关于修改计算信号不为0的涨跌幅的解释：
    原代码:
    data.loc[data['signal'] != 0, 'profit_pct'] = data['close'].pct_change()
    把没有买卖时的收益率也算上了,因此收益率profit_pct只是相比上一天的close比率
    这样是不对的，按照该策略(周四买，周一卖)，应该只计算周四买到周一卖时，这个时间
    段的收益率，即-1、1时的收益率，老师原本的才是正确的,即：
    data = data[data['signal'] != 0]    # data这里已经被筛选成-1，1的close了
    data['profit_pct'] = data['close'].pct_change()
    那个同学的是错的,之后老师改成了错的。
    老师改成错误的原因，是老师证明那个同学的代码时，证明的时候使用了错误的证明:
    老师把calculate_prof_pct和calculate_prof_pct2连着
    放在一起论证，导致了最终结果一致（详细见课程里3-6debug）
    """
    # 筛选信号不为0的，并且计算涨跌幅
    data['profit_pct'] = data.loc[data['signal'] != 0, 'close'].pct_change()
    data = data[data['signal'] == -1]  # 筛选平仓后的数据：单次收益
    return data


def calculate_cum_prof(data):
    """
    计算累计收益率（个股收益率）
    :param data: dataframe
    :return:
    """
    # 累计收益
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data


def caculate_portfolio_return(data, signal, n):
    """
    计算组合收益率
    :param data: dataframe
    :param signal: dataframe
    :param n: int
    :return returns: dataframe
    """
    returns = data.copy()
    # 投组收益率（等权重）= 收益率之和 / 股票个数
    returns['profit_pct'] = (signal * returns.shift(-1)).T.sum() / n
    returns = calculate_cum_prof(returns)
    return returns.shift(1)  # 匹配对应的交易月份


def caculate_max_drawdown(data, window=252):
    """
    计算最大回撤比
    :param data:
    :param window: int, 时间窗口设置，默认为252（日k）
    :return:
    """
    # 模拟持仓金额：投入的总金额 *（1+收益率）
    data['close'] = 10000 * (1 + data['cum_profit'])
    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window=window, min_periods=1).max()
    # 计算当天的回撤比 = (谷值 — 峰值)/峰值 = 谷值/峰值 - 1
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大的回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window, min_periods=1).min()

    return data


def calculate_sharpe(data):
    """
    计算夏普比率，返回的是年化的夏普比率
    :param data: dataframe, stock
    :return: float
    """
    # 公式：sharpe = (回报率的均值 - 无风险利率) / 回报率的标准差
    # daily_return = data['close'].pct_change()  # 演示部分
    daily_return = data['profit_pct']  # 策略应用后
    avg_return = daily_return.mean()
    sd_reutrn = daily_return.std()
    # 计算夏普：每日收益率 * 252 = 每年收益率
    sharpe = avg_return / sd_reutrn
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year
