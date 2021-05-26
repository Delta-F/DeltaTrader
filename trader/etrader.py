#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: etrader.py
@time: 2021/5/19 22:17
@desc:
'''

# 可能的不兼容情况：no module name win32api
# 版本调整以解决不兼容：python 3.7.x - pywin32 221-223
import easytrader

# 设置客户端信息（同花顺）
user = easytrader.use('ths')

# 连接客户端（同花顺：登录且保存密码且自动登录）
user.connect(r'C:\同花顺软件\同花顺\xiadan.exe')  # 类似 r'C:\htzqzyb2\xiadan.exe'

# 设置客户端编辑文本形式：type_keys
user.enable_type_keys_for_editor()

# 调用常用函数

# 一类：查询类
# 查询持仓
balance = user.balance
print(balance)
# 查询持仓（仓位）
position = user.position
print(position)

# 二类：交易
# 买入
# buy_no = user.buy('000002', price=26.78, amount=100)
# print(buy_no)
# 卖出
sell_no = user.buy('000001', price='', amount=100)
print(sell_no)
# 撤单：根据单号撤销，不稳定有效，待解决
# cancel = user.cancel_entrust('')
# print(cancel)
# 撤单：全部撤销
# cancel = user.cancel_all_entrusts()
# print(cancel)

# 查询当日成交
today_trades = user.today_trades
print(today_trades)
# 查询当日委托
today_entrusts = user.today_entrusts
print(today_entrusts)

