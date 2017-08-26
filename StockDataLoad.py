import os
import pandas as pd

def load_ma(df, n, field, column_name):
    df[column_name+str(n)] = df[field].rolling(window=n).mean()

def load_price_ma(df, n):
    load_ma(df, n, 'close', 'ma')

def load_volumn_ma(df, n):
    load_ma(df, n, 'volumn', 'v_ma')

def load_ema(df, n, field, column_name):
    df[column_name+str(n)] = df[field].ewm(span=n).mean()

def load_price_ema(df, n):
    load_ema(df, n, 'close', 'ema')

def load_volumn_ema(df, n):
    load_ema(df, n, 'volumn', 'v_ema')

def load_lines2df(lines):
    stock_lst = []
    for line in lines:
        stock_lst.append(line.split())

    df = pd.DataFrame(data=stock_lst, columns=['date', 'open', 'high', 'low', 'close', 'volumn', 'transation'])
    df.set_index(['date'], inplace=True)
    df = df.apply(pd.to_numeric, errors='coerce')

    load_price_ma(df, 5)
    load_price_ma(df, 20)
    load_price_ma(df, 60)

    load_price_ema(df, 5)
    load_price_ema(df, 20)
    load_price_ema(df, 60)

    load_volumn_ma(df, 5)

    load_volumn_ema(df, 5)

    return df

def load_file2lines(file_path):
    in_file = open(file_path)
    lines   = in_file.readlines()
    in_file.close()

    return lines[2:-1]

def load_file2df(file_path):
    return load_lines2df(load_file2lines(file_path))

def load_path2dict(path):
    if os.path.isdir(path) == False:
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
        stock_dict[stock_code]   = load_file2df(full_path)
        # print("Add "+stock_code)
    return stock_dict
