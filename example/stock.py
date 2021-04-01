#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: stock.py
@time: 2021/3/5 02:08
@desc: 获取价格，并且计算涨跌幅
'''

import data.stock as st

# 本地读取数据
data = st.get_csv_price('000002.XSHE', '2020-01-01', '2020-02-01')
print(data)
exit()  # 终端程序

# 获取平安银行的行情数据（日K）
data = st.get_single_price('000001.XSHE', 'daily', '2020-01-01', '2020-02-01')
# print(data)

# 计算涨跌幅，验证准确性
# data = st.calculate_change_pct(data)
# print(data)  # 多了一列close_pct

# 获取周K
data = st.transfer_price_freq(data, 'w')
print(data)

# 计算涨跌幅，验证准确性
data = st.calculate_change_pct(data)
print(data)  # 多了一列close_pct
