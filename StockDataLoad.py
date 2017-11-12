import os
import datetime
import pandas as pd

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

    stock_frame['close_pc'] = stock_frame['close'].pct_change()
    stock_frame['volume_pc'] = stock_frame['volume'].pct_change()
    stock_frame['ma5_pc'] = stock_frame['ma5'].pct_change()
    stock_frame['v_ma5_pc'] = stock_frame['v_ma5'].pct_change()
    stock_frame['rise_pc'] = (stock_frame['close'] - stock_open_shift)/stock_open_shift
    stock_frame['amplitude'] = (stock_frame['high'] - stock_frame['low'])/stock_frame['low']


def load_lines2df(lines, date_str_start=None, date_str_end=None):
    stock_lst = []
    start = None
    end = None

    if date_str_start is not None:
        start = datetime.datetime.strptime(date_str_start, '%Y/%m/%d')

    if date_str_end is not None:
        end = datetime.datetime.strptime(date_str_end, '%Y/%m/%d')

    for line in lines:
        field_list = line.split()

        if start is not None and start > datetime.datetime.strptime(field_list[0], '%Y/%m/%d'):
            continue

        if end is not None and end <= datetime.datetime.strptime(field_list[0], '%Y/%m/%d'):
            break

        stock_lst.append(field_list)

    df = pd.DataFrame(data=stock_lst, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'transation'])
    df.set_index(['date'], inplace=True)
    df = df.apply(pd.to_numeric, errors='coerce')

    load_price_ma(df, 5)
    # load_price_ma(df, 20)
    # load_price_ma(df, 60)

    # load_price_ema(df, 5)
    # load_price_ema(df, 20)
    # load_price_ema(df, 60)

    load_volume_ma(df, 5)

    # load_volume_ema(df, 5)

    load_preliminary_data(df)

    return df


def load_file2lines(file_path):
    in_file = open(file_path)
    lines   = in_file.readlines()
    in_file.close()

    return lines[2:-1]


def load_file2df(file_path, date_str_start=None, date_str_end=None):
    return load_lines2df(load_file2lines(file_path), date_str_start, date_str_end)


def load_path2dict(path, date_str_start=None, date_str_end=None):
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
        stock_dict[stock_code]   = load_file2df(full_path, date_str_start, date_str_end)
        # print("Add "+stock_code)
    return stock_dict
