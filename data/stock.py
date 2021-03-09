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

auth('username', 'password')  # 账号是申请时所填写的手机号
# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 1000)

# 全局变量
data_root = '/Users/ztnn/PycharmProjects/DeltaTrader/data/'


def get_stock_list():
    """
    获取所有A股股票列表
    上海证券交易所.XSHG
    深圳证券交易所.XSHE
    :return: stock_list
    """
    stock_list = list(get_all_securities(['stock']).index)
    return stock_list


def get_single_price(code, time_freq, start_date, end_date):
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
    # 获取行情数据
    data = get_price(code, start_date=start_date, end_date=end_date,
                     frequency=time_freq, panel=False)  # 获取获得在2015年
    return data


def export_data(data, filename, type):
    """
    导出股票相关数据
    :param data:
    :param filename:
    :param data: 股票数据类型，可以是：price、finance
    :return:
    """
    file_root = data_root + type + '/' + filename + '.csv'
    data.index.names = ['date']
    data.to_csv(file_root)  # 判断一下file是否存在 > 存在：追加 / 不存在：保持
    print('已成功存储至：', file_root)


def get_csv_data(code, type):
    file_root = data_root + type + '/' + code + '.csv'
    return pd.read_csv(file_root)


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
