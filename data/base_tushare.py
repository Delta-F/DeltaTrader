#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
 @Time : 2021/5/25 0:41
 @Author : xfcy
 @Version：V 0.1
 @File : base_tushare.py
 @desc :  利用tushare获取数据，更新接口的基本功能封装
 @IDL:
 1. 基础信息获取：
    1.1 股票列表--->获取股票代码，股票名称，tushare中的唯一字段
    1.2 交易日历--->判断今天是否是交易日
 2. 行情数据
    2.1 日线数据：包括但不限于股票基础数据（开高低收量额）
 @Step:
 1. 使用anaconda prompt 输入pip install tushare
 2. 到维护平台进行注册：https://tushare.pro/register?reg=400208
 3. 登录成功后，点击右上角->个人主页，在“用户中心”中点击“接口TOKEN”，复制token。
 ******************************************注意*****************************************
   token是调取数据的唯一凭证，请妥善保管，如发现别人盗用，可在本页面点击“刷新”操作，之前的token将失效。
 ***************************************************************************************

"""
import datetime

import util  # 因为我的token存于util.__init__.py中，所以我这里只想引入后得到token
import tushare as ts
import pandas as pd

# 1. 初始化tushare
ts.set_token(util.my_token)
api = ts.pro_api()


def get_stock_list():
    """
    获取所有A股列表
    :return: pd.DataFrame向量包括ts_code     symbol     name
    .SZ结尾表示深交所
    .SH结尾表示上交所
    """
    data = api.query(api_name="stock_basic", exchange="", list_status="L", fields="ts_code,symbol,name")
    return data


stock_df = get_stock_list()  # 先存储在内存中


def _get_ts_code_list():
    """
    获取ts_code
    :return: list : ts_code
    """
    return list(stock_df["ts_code"])


ts_code = _get_ts_code_list()  # 先存储在内存中


def get_code_by_name(name: str):
    """
    通过股票名称获取股票代码
    :param name: 股票名称
    :return: 股票代码
    """
    idx = stock_df[stock_df["name"] == name].index
    return list(stock_df.iloc[idx]["symbol"])[0]


def get_name_by_code(code: str):
    """
    通过股票代码获取股票名称
    :param code: 股票代码，需要字符串类型，可以加个断言，以0或6开头
    :return: 股票名称
    """
    idx = stock_df[stock_df["symbol"] == code].index
    return list(stock_df.iloc[idx]["name"])[0]


def get_ts_code(name: str = None, code: str = None):
    """
    获取股票的ts_code
    :param name: 股票名称
    :param code: 股票代码
    :return: ts的唯一标识
    """
    if name is None:
        idx = stock_df[stock_df["symbol"] == code].index
    else:
        idx = stock_df[stock_df["name"] == name].index
    return list(stock_df.iloc[idx]["ts_code"])[0]


def today_is_trading_day():
    """
    判断今天是否是交易日：单支股票判断今天是否交易，避免了节假日获取，停牌获取等无法获取的自然因素，使得数据更加干净
    :return: bool
    """
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    data = api.query(api_name="trade_cal", start_date=today_date, end_date=today_date)
    if data.iat[0, 2] == 1:
        return True
    else:
        return False


def get_single_today(ts_code: str):
    """
    获取单支股票今日数据
    :param ts_code: 必须是ts的股票唯一标识
    :return:向量包括ts_code     trade_date  open  high   low  close  pre_close  change    pct_chg  vol     amount
    """
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    if today_is_trading_day():
        df = api.query(api_name="daily", ts_code=ts_code, trade_date=today_date)
        return df
    else:
        print("今天不是交易日")
        exit()


def get_single_history(ts_code: str):
    """
    获取某只股票截止今日（若今日未完成则是上一个交易日）的数据
    :param ts_code:必须是ts的股票唯一标识
    :return: pd.DataFrame包含20000215开始的数据，向量包括ts_code     trade_date  open  high   low  close  pre_close  change    pct_chg  vol     amount
    """
    if today_is_trading_day():
        df = api.query(api_name="daily", ts_code=ts_code)
        return df
    else:
        print("今天不是交易日")
        exit()

