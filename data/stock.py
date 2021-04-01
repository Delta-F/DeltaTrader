#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: Stock.py
@time: 2021/2/22 23:21
@desc:
'''

from jqdatasdk import *
import time
import pandas as pd
import datetime
import os

auth('username', 'password')  # 账号是申请时所填写的手机号
# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 1000)

# 全局变量
data_root = '/Users/ztnn/PycharmProjects/DeltaTrader/data/'


def init_db():
    '''
    初始化股票数据库
    :return:
    '''
    # 1.获取所有股票代码
    stocks = get_stock_list()
    # 2.存储到csv文件中
    for code in stocks:
        df = get_single_price(code, 'daily')
        export_data(df, code, 'price')
        print(code)
        print(df.head())


def get_stock_list():
    """
    获取所有A股股票列表
    上海证券交易所.XSHG
    深圳证券交易所.XSHE
    :return: stock_list
    """
    stock_list = list(get_all_securities(['stock']).index)
    return stock_list


def get_single_price(code, time_freq, start_date=None, end_date=None):
    """
    获取单个股票行情数据
    :param code: 
    :param time_freq: 
    :param start_date: 
    :param end_date: 
    :return: 
    """
    # 如果start_date=None，默认为从上市日期开始
    if start_date is None:
        start_date = get_security_info(code).start_date
    if end_date is None:
        end_date = datetime.datetime.today()
    # 获取行情数据
    data = get_price(code, start_date=start_date, end_date=end_date,
                     frequency=time_freq, panel=False)  # 获取获得在2015年
    return data


def export_data(data, filename, type, mode=None):
    """
    导出股票相关数据
    :param data:
    :param filename:
    :param type: 股票数据类型，可以是：price、finance
    :param mode: a代表追加，none代表默认w写入
    :return:
    """
    file_root = data_root + type + '/' + filename + '.csv'
    data.index.names = ['date']
    if mode == 'a':
        data.to_csv(file_root, mode=mode, header=False)
        # 删除重复值
        data = pd.read_csv(file_root)  # 读取数据
        data = data.drop_duplicates(subset=['date'])  # 以日期列为准
        data.to_csv(file_root, index=False)  # 重新写入
    else:
        data.to_csv(file_root)  # 判断一下file是否存在 > 存在：追加 / 不存在：保持

    print('已成功存储至：', file_root)


def get_csv_price(code, start_date, end_date):
    """
    获取本地数据，且顺便完成数据更新工作
    :param code: str,股票代码
    :param start_date: str,起始日期
    :param end_date: str,起始日期
    :return: dataframe
    """
    # 使用update直接更新
    update_daily_price(code)
    # 读取数据
    file_root = data_root + 'price/' + code + '.csv'
    data = pd.read_csv(file_root, index_col='date')
    # print(data)
    # 根据日期筛选股票数据
    return data[(data.index >= start_date) & (data.index <= end_date)]


def transfer_price_freq(data, time_freq):
    """
    将数据转换为制定周期：开盘价（周期第1天）、收盘价（周期最后1天）、最高价（周期内）、最低价（周期内）
    :param data:
    :param time_freq:
    :return:
    """
    df_trans = pd.DataFrame()
    df_trans['open'] = data['open'].resample(time_freq).first()
    df_trans['close'] = data['close'].resample(time_freq).last()
    df_trans['high'] = data['high'].resample(time_freq).max()
    df_trans['low'] = data['low'].resample(time_freq).min()

    return df_trans


def get_single_finance(code, date, statDate):
    """
    获取单个股票财务指标
    :param code:
    :param date:
    :param statDate:
    :return:
    """
    data = get_fundamentals(query(indicator).filter(indicator.code == code), date=date, statDate=statDate)  # 获取财务指标数据
    return data


def get_single_valuation(code, date, statDate):
    """
    获取单个股票估值指标
    :param code:
    :param date:
    :param statDate:
    :return:
    """
    data = get_fundamentals(query(valuation).filter(valuation.code == code), date=date, statDate=statDate)  # 获取财务指标数据
    return data


def calculate_change_pct(data):
    """
    涨跌幅 = (当期收盘价-前期收盘价) / 前期收盘价
    :param data: dataframe，带有收盘价
    :return: dataframe，带有涨跌幅
    """
    data['close_pct'] = (data['close'] - data['close'].shift(1)) \
                        / data['close'].shift(1)
    return data


def update_daily_price(stock_code, type='price'):
    # 3.1是否存在文件：不存在-重新获取，存在->3.2
    file_root = data_root + type + '/' + stock_code + '.csv'
    if os.path.exists(file_root):  # 如果存在对应文件
        # 3.2获取增量数据（code，startsdate=对应股票csv中最新日期，enddate=今天）
        startdate = pd.read_csv(file_root, usecols=['date'])['date'].iloc[-1]
        df = get_single_price(stock_code, 'daily', startdate, datetime.datetime.today())
        # 3.3追加到已有文件中
        export_data(df, stock_code, 'price', 'a')
    else:
        # 重新获取该股票行情数据
        df = get_single_price(stock_code, 'daily')
        export_data(df, stock_code, 'price')

    print("股票数据已经更新成功：", stock_code)


if __name__ == '__main__':
    # data = get_fundamentals(query(indicator), statDate='2020')  # 获取财务指标数据
    # print(data)

    df = get_fundamentals(query(valuation), date='2021-03-24')
    print(df)
