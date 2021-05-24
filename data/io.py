# -*- coding: utf-8 -*-#
"""
@File    :   io.py    
@Contact :   sheng_jun@yeah.net
@Author  :   Ace
@Description: 
@Modify Time      @Version    @Desciption
------------      --------    -----------
2021-04-27 14:31    1.0         None
"""

import pandas as pd
import os
import datetime

daily_root = "D:\\basic-trading-data\\stock_data_daily\\"


def get_stock_path(code):
    """
    得到股票存储绝对路径(吐槽：python的相对路径有点太搞人了)
    :param code:拼接得到唯一文件名
    :return:str：文件路径
    """
    path = daily_root + code + ".csv"
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


def get_stock_list():
    """
    获得本地股票代码列表
    :return:股票代码
    """
    file_location = "D:\\basic-trading-data\\stock_data_daily"
    file_names = []
    for roots, dirs, files in os.walk(file_location):
        for filename in files:
            if filename.endswith(".csv"):
                filename = filename.split(".")[0]
                file_names.append(filename)
    return file_names


def get_stock_code_name_2_csv():
    """
    存储股票代码和名称
    :return:
    """
    code_list = get_stock_list()
    name_list = []
    for code in code_list:
        df = read_stock_from_csv(code)
        name = df.iloc[-1]["name"]  # 有的股票会更名，我们使用最新的名称
        name_list.append(name)
    df = pd.DataFrame(data={"code": code_list, "name": name_list})
    path = 'D:\\basic-trading-data\\name_code.csv'
    df.to_csv(path_or_buf=path, encoding="gbk", index=False, mode="w")
    print("已将股票名称和代码存储至", path)


def _read_name_code_df():
    """
    读取股票名称和代码
    :return:
    """
    path = 'D:\\basic-trading-data\\name_code.csv'
    df = pd.read_csv(filepath_or_buffer=path, encoding="gbk")
    return df


def get_name_by_code(code: str):
    """
    通过代码获取股票名称
    :param code: 股票代码
    :return: 股票名称
    """
    df = _read_name_code_df()
    index = df[df["code"] == code].index
    return df.iloc[index]["name"][0]


def get_code_by_name(name: str):
    """

    :param name:
    :return:
    """
    df = _read_name_code_df()
    index = df[df["name"] == name].index
    return list(df.iloc[index]["code"])[0]


def read_stock_from_csv(code):
    """

    :param code:
    :return:
    """
    stock_path = get_stock_path(code)
    df = pd.read_csv(
        filepath_or_buffer=stock_path,
        encoding="gbk",
        parse_dates=["date"]
    )
    # 强制去重，防止日期获取的重复
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values(by=["date"], inplace=True)
    df.drop_duplicates(subset=["date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def save_df_2_csv(df: pd.DataFrame, dirs, name: str):
    """

    :param df:
    :param dirs:
    :param name:
    :return:
    """
    path = "D:\\basic-trading-data\\" + dirs
    if not os.path.exists(path):
        os.mkdir(path)
    path += "\\" + name + ".csv"
    df.to_csv(path_or_buf=path, encoding="gbk", index=False, mode="w")
    print("文件已存入", path)


def read_df_from_csv(dirs: str, name: str):
    """
    :param dirs:
    :param name:
    :return:
    """
    path = "D:\\basic-trading-data\\" + dirs + "\\" + name + ".csv"
    if not os.path.exists(path):
        print("文件不存在")
        return
    df = pd.read_csv(
        filepath_or_buffer=path,
        encoding="gbk"
    )
    return df


def save_df_2_hdf(df: pd.DataFrame, dirs: str, file_name: str, key: str):
    """

    :param df:
    :param dirs:
    :param file_name:
    :param key:
    :return:
    """
    path = "D:\\basic-trading-data\\" + dirs
    if not os.path.exists(path):
        os.mkdir(path)
    path += "\\" + file_name + ".h5"
    h5_store = pd.HDFStore(
        path,
        mode="w"
    )
    h5_store[key] = df
    h5_store.close()
    print("文件已存入", path)


def read_df_from_hdf(dirs: str, file_name: str, key: str):
    """

    :param dirs:
    :param file_name:
    :param key:
    :return:
    """
    path = "D:\\basic-trading-data\\" + dirs + "\\" + file_name + ".h5"
    if not os.path.exists(path):
        print("文件不存在")
        return
    print(path)
    h5 = pd.HDFStore(
        path,
        mode="r"
    )
    df = h5.get(key)
    h5.close()
    return df


def save_all_stock_2_hdf():
    """
    :return:
    """
    path = "D:\\basic-trading-data\\stock_data_daily\\"
    file_name = str(datetime.datetime.today()).split(" ")[0]
    path += file_name + ".h5"
    h5_store = pd.HDFStore(
        path,
        mode="w"
    )
    code_list = get_stock_list()
    for code in code_list:
        df = read_stock_from_csv(code)
        h5_store[code] = df
        print(code + "已存入" + path)
    h5_store.close()


