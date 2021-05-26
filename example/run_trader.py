#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: PyCharm
@file: DeltaTrader -> run_trader
@time: 2021/5/21 7:18
@desc: 以双均线策略为例，进行模拟实盘交易
'''
import time

import data.stock as st
import strategy.ma_strategy as ma
import easytrader
import pandas as pd

# 交易初始化
user = easytrader.use('ths')
user.connect(r'C:\同花顺软件\同花顺\xiadan.exe')  # 类似 r'C:\htzqzyb2\xiadan.exe'
user.enable_type_keys_for_editor()

# 参数设置
start_date = '2016-01-01'
end_date = '2021-5-21'

# step1：确定股票池：大盘股，沪深300
stocks = st.get_index_list()  # 默认获取沪深300
# print("========股票列表：", stocks)

# step2：找到有交易信号的股票，为之后交易进行准备
for stock in stocks:
    data = st.get_csv_price(stock, start_date, end_date)  # 获取本地数据（同时完成更新）
    print("========股票数据：", stock)

    # 跑策略：双均线
    data = ma.ma_strategy(data)
    print(data.tail())

    # step3：判断交易信号：买入、卖出
    signal = data['signal'].iloc[-1]
    print("========交易信号：", signal)

    # 交易参数设置
    code = stock.split('.')[0]  # 000001.XSHE -> 000001
    price = data['close'].iloc[-1]  # 获取当期收盘价
    amount = 100

    # 获取持仓信息
    position = pd.DataFrame(user.position)  # 转化为dataframe
    stock_pos = position[position['证券代码'] == '000001']['可用余额'].iloc[0]
    print("========最新持仓：", position)

    # 进行买入、卖出操作
    if signal == 1:  # 买入
        entrust = user.buy(code, price, amount)
        print("========买入id：", entrust)
    elif signal == -1 and stock_pos is not None:
        entrust = user.sell(code, price, stock_pos)
        print("========卖出id：", entrust)
    else:
        print("无交易")

    time.sleep(3)
# step4：容错处理、提示信息
