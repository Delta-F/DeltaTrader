# -*- coding: utf-8 -*-#
"""
@File    :   upgrade.py    
@Contact :   gopheriilidan@yeah.net
@Author  :   Ace
@Description: 
@Modify Time      @Version    @Desciption
------------      --------    -----------
2021-04-26 8:40    1.0         None
@ Todo:需要更新解决数据存储绝对路径的问题
"""
import os
import time
import datetime
import random
import pandas as pd
import urllib.request as request
import json
import numpy as np

root = "D:\\basic-trading-data\\stock_data\\"


def get_content_from_internet(url):
    """
    从指定的url获取数据
    :param url:
    :return: str:页面内容
    """
    max_try = 10
    timeout = 15
    wait_time = 10
    flag = False
    for i in range(max_try):
        try:
            content = request.urlopen(url, timeout=timeout).read()
            flag = True
            break
        except Exception as e:
            print("获取数据失败第", i + 1, "次，报错内容：", e)
            time.sleep(wait_time)
    if flag:
        return content
    else:
        raise ValueError("获取数据url不停报错，停止运行!")


def get_latest_trade_date():
    """
    获取最近的交易日期
    :return: str:"%Y-%m-%d"格式的日期
    """
    url = "http://hq.sinajs.cn/rn=34101&list=sh000001"
    content: str = get_content_from_internet(url).decode("gbk")
    content_list = content.split(",")
    return content_list[-4]


def get_daily_stock():
    """
    网址：http://vip.stock.finance.sina.com.cn/mkt/#stock_hs_up
        后台网址(json格式数据)：http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=symbol&asc=1&node=hs_a&symbol=&_s_r_a=sort
            数据回显： http://hq.sinajs.cn/rn=34101&list=sz300325,sz300141,sz300563,sh688068,sh688686,sh688699,sz300671,sz300015,sz300677,sh688468,sz000150,sz002665,sz002630,sz002587,sh600172,sz002168,sh603316,sh600581,sh601126,sh600149,sh601038,sz000929,sz002885,sh605016,sz002997,sz002763,sz002340,sz002786,sh605117,sh603538,sh603698,sh605369,sh605098,sh603444,sz002071,sz002240,sz002901,sh605177,sh605086,sh601127
    :return: pd.DataFrame当天A股市场的交易数据，我们按照数据模板：["code","name","date","open","high","low","close","ex_close","volume","money"]进行数据整合
    """
    ori_url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=%s&num=40&sort=symbol&asc=1&node=hs_a&symbol=&_s_r_a=sort"
    page_num = 1
    daily_all_df = pd.DataFrame()
    date = get_latest_trade_date()

    while True:
        # 拼接url
        # 获取网页内容：get_content_from_internet()
        # 判断是否是最后一页，这里找到的方法是：len(content) < 3证明是最后一页
        # 解析json数据
        # 将解析好的数据变形为DataFrame
        # 整理数据
        # 当天没有数据（这个网站没有已经关闭的股票信息，但是有停牌的）的股票
        # page_num++
        print("获取第", page_num, "页的数据")
        url = ori_url % (page_num)
        content = get_content_from_internet(url).decode("gbk")
        if len(content) < 3:
            print("数据获取完毕")
            break
        json_loads = json.loads(content)
        df = pd.DataFrame(json_loads, dtype="float")
        # 这里的股票代码是symbol
        # 列向量名称：["code","name","date","open","high","low","close","ex_close","volume","money"]
        df = df[["symbol", "name", "open", "high", "low", "trade", "settlement", "volume", "amount"]]
        # 改名
        new_name_map = {
            "symbol": "code",
            "trade": "close",
            "settlement": "ex_close",
            "amount": "money"
        }
        # 数据中缺少交易日，需要单独获取
        df["date"] = date
        df.rename(columns=new_name_map, inplace=True)

        # 整理数据：
        df = df[["code", "name", "date", "open", "high", "low", "close", "ex_close", "volume", "money"]]
        # return df

        # 合并数据
        daily_all_df = daily_all_df.append(df, ignore_index=True)
        page_num += 1
        time.sleep(1)
    daily_all_df = daily_all_df[daily_all_df["open"] - 0 > 0.00000000001]
    daily_all_df.reset_index(drop=True, inplace=True)
    return daily_all_df


def get_stock_path(code):
    """
    得到股票存储绝对路径(吐槽：python的相对路径有点太搞人了)
    :param code:拼接得到唯一文件名
    :return:str：文件路径
    """
    path = root + code + ".csv"
    return path


def save_today_data_2_csv(df: pd.DataFrame):
    """
    存储今日的A股数据
    :param df: 获得的A股数据
    :return:
    """
    num = 1
    for i in df.index:
        current_df: pd.DataFrame = df.iloc[[i]]
        current_stock = current_df.iloc[0]["code"]
        # 获取股票路径 get_stock_path(code)
        file_path = get_stock_path(current_stock)
        # 如果文件存在，说明是新股
        if os.path.exists(file_path):
            current_df.to_csv(
                path_or_buf=file_path,
                header=None,
                index=False,
                mode="a",
                encoding="gbk",
            )
        # 文件不存在，说明是新股
        else:
            current_df.to_csv(path_or_buf=file_path, index=False, mode="a", encoding="gbk")
        print(current_stock, "已存储到：", file_path)
        num += 1
    print(num, "支股票已存入.csv文件")


def read_data_frame_from_csv(code):
    stock_path = get_stock_path(code)
    df = pd.read_csv(
        filepath_or_buffer=stock_path,
        encoding="gbk",
    )
    return df


def uniform_vector_standard(code):
    """
    将所有信息的vector统一
    :param code:
    :return: 统一向名称
    """
    path = get_stock_path(code)
    df = pd.read_csv(
        filepath_or_buffer=path,
        skiprows=1,
        encoding="gbk"
    )
    uniform_name_map = {
        "股票代码": "code",
        "股票名称": "name",
        "交易日期": "date",
        "开盘价": "open",
        "最高价": "high",
        "最低价": "low",
        "收盘价": "close",
        "前收盘价": "ex_close",
        "成交量": "volume",
        "成交额": "money"
    }
    df.rename(columns=uniform_name_map, inplace=True)
    df.to_csv(path_or_buf=path, index=False, mode="w", encoding="gbk")
    print(path, "的内容已改变")


def get_stock_list():
    """
    获得本地股票代码列表
    :return:股票代码
    """
    file_location = "D:\\basic-trading-data\\stock_data"
    file_names = []
    for roots, dirs, files in os.walk(file_location):
        for filename in files:
            if filename.endswith(".csv"):
                filename = filename.split(".")[0]
                file_names.append(filename)
    return file_names


def today_is_trading_day():
    """
    判断今天是否是交易日
    :return: bool
    """
    return datetime.datetime.now().strftime("%Y-%m-%d") == get_latest_trade_date()


def random_16(n=16):
    """
    生成一个16位的随机数
    :param n:
    :return:
    """
    start = 10 ** (n - 1)
    end = (10 ** n) - 1
    return str(random.randint(start, end))


def get_appointed_date_single_stock(code: str, date: str):
    """
    最长可以获取2年的数据
    :param code:股票代码
    :param date:选择的日期
    :return:pd.DataFrame返回指定日期的数据
    """
    k_type = "day"
    num = 640  # 好像超过某个值是无法获取的
    url = "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_%sqfq&param=%s,%s,,,%s,qfq&r=0.%s"
    url = url % (k_type, code, k_type, num, random_16())
    content = get_content_from_internet(url).decode("gbk")
    content = content.split("=")[-1]
    content = json.loads(content)
    # 观察数据之后发现总共有3个节点是没用的
    data = content["data"][code]
    # 取了多支股票观察后发现，有个 qfq的前缀+k_type构成
    key = "qfq" + k_type
    data = data[key]
    # return data
    # 观察后得到data是一个二维数组
    df = pd.DataFrame(data)
    # return df
    # 对比整理数据得到
    name_map = {
        0: "date",
        1: "open",
        2: "close",
        3: "high",
        4: "low",
        5: "money",
        6: "info"
    }
    df.rename(columns=name_map, inplace=True)
    if "info" not in df:
        df["info"] = None
    # 数据形状：["code", "name", "date", "open", "high", "low", "close", "ex_close", "volume", "money"]
    df["code"] = code
    df["name"] = np.NAN
    df["ex_close"] = np.NAN
    df["volume"] = np.NAN
    df = df[["code", "name", "date", "open", "high", "low", "close", "ex_close", "volume", "money"]]
    df_result = df[df["date"] == date]
    return df_result
