#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: statistical_test.py
@time: 2021/3/30 22:00
@desc:
'''
import data.stock as st
import strategy.ma_strategy as ma
import matplotlib.pyplot as plt
from scipy import stats


def ttest(data_return):
    """
    对策略收益进行t检验
    :param strat_return: dataframe,单次收益率
    :return: float,t值和p值
    """
    # 调用假设检验ttest函数：scipy
    t, p = stats.ttest_1samp(data_return, 0, nan_policy='omit')

    # 判断是否与理论均值有显著性差异:α=0.05
    p_value = p / 2  # 获取单边p值

    # 打印
    print("t-value:", t)
    print("p-value:", p_value)
    print("是否可以拒绝[H0]收益均值=0：", p_value < 0.05)

    return t, p_value


if __name__ == '__main__':
    # 股票列表
    stocks = ['000001.XSHE', '000858.XSHE', '002594.XSHE']
    for code in stocks:
        print(code)
        df = st.get_single_price(code, 'daily', '2016-12-01', '2021-01-01')
        df = ma.ma_strategy(df)  # 调用双均线策略

        # 策略的单次收益率
        returns = df['profit_pct']
        # print(returns)

        # 绘制一下分布图用于观察
        # plt.hist(returns, bins=30)
        # plt.show()

        # 对多个股票进行计算、测试
        ttest(returns)
