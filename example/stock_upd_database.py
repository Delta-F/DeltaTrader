#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: stock.py
@time: 2021/3/3 00:29
@desc: 用于调用股票行情数据的脚本
'''

import data.stock as st
import pandas as pd

# 初始化变量
code = '000001.XSHG'

# 调用一只股票的行情数据
data = st.get_single_price(code=code,
                           time_freq='daily',
                           start_date='2021-02-01',
                           end_date='2021-03-01')
# 存入csv
st.export_data(data=data, filename=code, type='price')

# 从csv中获取数据
data = st.get_csv_data(code=code, type='price')
print(data)

# 实时更新数据：假设每天更新日K数据 > 存到csv文件里面 > data.to_csv(append)
