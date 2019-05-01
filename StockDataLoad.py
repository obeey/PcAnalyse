import datetime
import math
import os

import numpy as np
import pandas as pd

SDL_TREND_SMALL = 5
SDL_TREND_MEDIUM = 10
SDL_TREND_LARGE = 20

def load_ma(df, n, field, column_name):
    df[column_name+str(n)] = df[field].rolling(window=n).mean()

def load_price_ma(df, n):
    load_ma(df, n, 'close', 'ma')

def load_volume_ma(df, n):
    load_ma(df, n, 'volume', 'v_ma')

def load_ema(df, n, field, column_name):
    df[column_name+str(n)] = df[field].ewm(span=n).mean()

def load_price_ema(df, n):
    load_ema(df, n, 'close', 'ema')

def load_volume_ema(df, n):
    load_ema(df, n, 'volume', 'v_ema')

def load_preliminary_data(stock_frame):
    stock_open_shift = stock_frame['open'].shift()

    stock_frame['open_pc'] = stock_frame['open'].pct_change()
    stock_frame['close_pc'] = stock_frame['close'].pct_change()
    stock_frame['volume_pc'] = stock_frame['volume'].pct_change()
    stock_frame['ma'+str(SDL_TREND_SMALL)+'_pc'] = stock_frame['ma'+str(SDL_TREND_SMALL)].pct_change()
    stock_frame['ma'+str(SDL_TREND_MEDIUM)+'_pc'] = stock_frame['ma'+str(SDL_TREND_MEDIUM)].pct_change()
    stock_frame['ma'+str(SDL_TREND_LARGE)+'_pc'] = stock_frame['ma'+str(SDL_TREND_LARGE)].pct_change()
    stock_frame['v_ma'+str(SDL_TREND_SMALL)+'_pc'] = stock_frame['v_ma'+str(SDL_TREND_SMALL)].pct_change()
    stock_frame['v_ma'+str(SDL_TREND_MEDIUM)+'_pc'] = stock_frame['v_ma'+str(SDL_TREND_MEDIUM)].pct_change()
    stock_frame['v_ma'+str(SDL_TREND_LARGE)+'_pc'] = stock_frame['v_ma'+str(SDL_TREND_LARGE)].pct_change()
    stock_frame['rise_pc'] = (stock_frame['close'] - stock_open_shift)/stock_open_shift
    stock_frame['amplitude'] = (stock_frame['high'] - stock_frame['low'])/stock_frame['low']
    price_range = (stock_frame['high'] - stock_frame['low'])
    price_range = price_range.replace(0, 100000)
    stock_frame['oc_pc'] = abs(stock_frame['close'] - stock_frame['open'])/price_range

from enum import Enum
class LoadDateFilterAction(Enum):
    CONTINUE = 0
    BREAK = 1
    PASS = 2
    
def load_filter_lines_action(lines, date_filter=None, data_action=None):
    stock_lst = []
    
    for line in lines:
        field_list = line.split()

        if float(field_list[1]) == 0 or float(field_list[2]) == 0 or float(field_list[3]) == 0 or float(field_list[4]) == 0 or float(field_list[5]) == 0 or float(field_list[6]) == 0 :
            continue

        stock_lst.append(field_list)

    df = pd.DataFrame(data=stock_lst, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'transation'])
    df.set_index(['date'], inplace=True)
    df = df.apply(pd.to_numeric, errors='coerce')

    df.index = pd.to_datetime(df.index, format='%Y/%m/%d')
    

    if data_action is not None:
        data_action(df)

    start_date = None
    end_date = None
    for date,value in df.iterrows():
        action = date_filter(date)
        if LoadDateFilterAction.CONTINUE == action:
            continue
        if start_date is None:
            start_date = date
        end_date = date
        
        if LoadDateFilterAction.BREAK == action:
            break

    return df[start_date:end_date]

def __load_filter_lines_date_range_action__(date_start, date_end):
    def date_range_action(date_current):
        if date_start > date_current:
            return LoadDateFilterAction.CONTINUE
        if date_current >= date_end:
            return LoadDateFilterAction.BREAK
        return LoadDateFilterAction.PASS
    if date_start is None and date_end is None:
        return lambda x : LoadDateFilterAction.PASS
    if date_start is None:
        return lambda x : LoadDateFilterAction.BREAK if x >= date_end else LoadDateFilterAction.PASS
    if date_end is None:
        return lambda x : LoadDateFilterAction.CONTINUE if x < date_start else LoadDateFilterAction.PASS
    return date_range_action

def __load_filter_lines_date_day_action__(date):
    def date_day_action(date_current):
        if date_current < date:
            return LoadDateFilterAction.CONTINUE
        if date_current > date:
            return LoadDateFilterAction.BREAK
        return LoadDateFilterAction.PASS
    if date is None:
        return lambda x : LoadDateFilterAction.PASS
    return date_day_action
        
def load_filter_lines_date(lines, date_str=None, data_action=None):
    date = datetime.datetime.strptime(date_str, '%Y/%m/%d')
    return load_filter_lines_action(lines, __load_filter_lines_date_day_action__(date), data_action)

def load_filter_lines_range(lines, start_date=None, end_date=None, data_action=None):
    start = None
    end = None
    if start_date is not None:
        start = datetime.datetime.strptime(start_date, '%Y/%m/%d')
    if end_date is not None:
        end = datetime.datetime.strptime(end_date, '%Y/%m/%d')
    return load_filter_lines_action(lines, __load_filter_lines_date_range_action__(start, end), data_action)

def load_lines2df(lines, start_date=None, end_date=None):
    stock_lst = []
    start = None
    end = None

    if start_date is not None:
        start = datetime.datetime.strptime(start_date, '%Y/%m/%d')

    if end_date is not None:
        end = datetime.datetime.strptime(end_date, '%Y/%m/%d')

    for line in lines:
        field_list = line.split()

        if start is not None and start > datetime.datetime.strptime(field_list[0], '%Y/%m/%d'):
            continue

        if end is not None and end <= datetime.datetime.strptime(field_list[0], '%Y/%m/%d'):
            break

        if float(field_list[1]) == 0 or float(field_list[2]) == 0 or float(field_list[3]) == 0 or float(field_list[4]) == 0 or float(field_list[5]) == 0 or float(field_list[6]) == 0 :
            continue

        stock_lst.append(field_list)

    df = pd.DataFrame(data=stock_lst, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'transation'])
    df.set_index(['date'], inplace=True)
    df = df.apply(pd.to_numeric, errors='coerce')

    load_price_ma(df, SDL_TREND_SMALL)
    load_price_ma(df, SDL_TREND_MEDIUM)
    load_price_ma(df, SDL_TREND_LARGE)

    # load_price_ema(df, 5)
    # load_price_ema(df, 20)
    # load_price_ema(df, 60)

    load_volume_ma(df, SDL_TREND_SMALL)
    load_volume_ma(df, SDL_TREND_MEDIUM)
    load_volume_ma(df, SDL_TREND_LARGE)

    # load_volume_ema(df, 5)

    load_preliminary_data(df)

    # df = df[np.isfinite(df['ma20_pc'])]

    return df


def load_file2lines(file_path):
    in_file = open(file_path)
    lines   = in_file.readlines()
    in_file.close()

    return lines[2:-1]


def load_file2df_range(file_path, start_date=None, end_date=None, data_action=None):
    return load_filter_lines_range(load_file2lines(file_path), start_date, end_date, data_action)

def load_file2df_day(file_path, date=None, data_action=None):
    return load_filter_lines_date(load_file2lines(file_path), date, data_action)

def load_path2dict(path, start_date=None, end_date=None, date=None, data_action=None):
    if not os.path.isdir(path):
        print("Not dir")
        return

    stock_dict = {}

    for f in os.listdir(path):
        full_path   = os.path.join(path,f)
        # if False == os.path.isfile(full_path):
        #     continue

        if ('SH#' != f[:3]) and ('SZ#' != f[:3]):
            continue
        # print(f)

        stock_code  = f[3:-4]
        if date is None:
            stock_dict[stock_code]   = load_file2df_range(full_path, start_date, end_date, data_action)
        else:
            stock_dict[stock_code]   = load_file2df_day(full_path, date, data_action)
        
        # print("Add "+stock_code)
    return stock_dict

def load_path2dict_date(path, date=None):
    if not os.path.isdir(path):
        print("Not dir")
        return

    stock_dict = {}

    for f in os.listdir(path):
        full_path   = os.path.join(path,f)
        # if False == os.path.isfile(full_path):
        #     continue

        if ('SH#' != f[:3]) and ('SZ#' != f[:3]):
            continue
        # print(f)

        stock_code  = f[3:-4]

        stock_dict[stock_code]   = load_file2df_day(full_path, date)
        
        # print("Add "+stock_code)
    return stock_dict

def load_path2dict_normalization(path, start_date=None, end_date=None):
    stock_dict = load_path2dict(path, start_date, end_date)

    for c, d in stock_dict.items():
        stock_dict[c] = load_normalization(d)

    return stock_dict

def load_normalization_from_dict(stock_dict):
    normalized = {}

    for c, d in stock_dict.items():
        # print(c)
        normalized[c] = load_normalization(d)

    return normalized

"""
df's format:
            open	high	low	close	volume	transation	ma5	ma20	v_ma5	v_ma10	close_pc	volume_pc	ma5_pc	ma20_pc	v_ma5_pc	v_ma10_pc	rise_pc	amplitude	oc_pc
date																			
2014/09/02	9.51	9.63	9.46	9.60	128705724	1.227884e+09	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	NaN	0.017970	0.529412
2014/09/03	9.63	9.74	9.62	9.68	128588110	1.244850e+09	NaN	NaN	NaN	NaN	0.008333	-0.000914	NaN	NaN	NaN	NaN	0.017876	0.012474	0.416667
2014/09/04	9.70	9.72	9.63	9.71	98919202	9.567538e+08	NaN	NaN	NaN	NaN	0.003099	-0.230728	NaN	NaN	NaN	NaN	0.008307	0.009346	0.111111
2014/09/05	9.73	9.78	9.69	9.74	126925907	1.234562e+09	NaN	NaN	NaN	NaN	0.003090	0.283127	NaN	NaN	NaN	NaN	0.004124	0.009288	0.111111
2014/09/09	9.75	9.82	9.68	9.70	123866063	1.205606e+09	9.686	NaN	121401001.2	NaN	-0.004107	-0.024107	NaN	NaN	NaN	NaN	-0.003083	0.014463	0.357143
"""
def load_normalization(df):
    colume_max  = df.max(axis=0)

    # print(colume_max)
    colume_max = colume_max.apply(lambda x : math.ceil(x))
    df = (df+colume_max)/(colume_max*2)

    return df
