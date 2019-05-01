from datetime import datetime
from datetime import timedelta
from datetime import date
import pandas as pd

def kline_sharp_crossStar(open, close, high, low):
    OCPC_THRELDHOLD = 0.001
    OLPC_THRELDHOLD = 0.025
    AR_THRELDHOLD = 4

    if 0 == open:
        return False

    ocpc = abs(close - open)/open
    olpc = abs(open - low )/open

    # print("\t{}\t{}".format(ocpc, olpc))

    if ocpc < 0.01:
        if olpc > OLPC_THRELDHOLD:
            return True
        else:
            return False

    amplitude_rate = olpc/ocpc

    if ocpc < OCPC_THRELDHOLD and amplitude_rate > AR_THRELDHOLD:
        return True

    return False

import StockDataLoad as sdl

def kline_sharp_action_ma(df):
    sdl.load_price_ma(df, sdl.SDL_TREND_SMALL)
    sdl.load_price_ma(df, sdl.SDL_TREND_MEDIUM)
    sdl.load_price_ma(df, sdl.SDL_TREND_LARGE)

    # load_price_ema(df, 5)
    # load_price_ema(df, 20)
    # load_price_ema(df, 60)

    sdl.load_volume_ma(df, sdl.SDL_TREND_SMALL)
    sdl.load_volume_ma(df, sdl.SDL_TREND_MEDIUM)
    sdl.load_volume_ma(df, sdl.SDL_TREND_LARGE)

    # load_volume_ema(df, 5)

    sdl.load_preliminary_data(df)
    
def kline_sharp_day(stock_dict, date_str):
    date = datetime.strptime(date_str, '%Y/%m/%d')
    __kline_sharp_day__(stock_dict, date)
    
def kline_sharp_range(stock_dict, start_str=None, end_str=None):
    if start_str is None:
        start_str = '1997/04/30'
    start = datetime.strptime(start_str, '%Y/%m/%d')
    if end_str is None:
        end = date.today() + timedelta(days=1)
    else:
        end = datetime.strptime(end_str, '%Y/%m/%d')
    
        
    dates = pd.bdate_range(start, end).tolist()
    for d in dates:
        stocks = __kline_sharp_day__(stock_dict, d)
        if len(stocks) > 0:
            print(d.strftime("%Y-%m-%d"))
            for s in stocks:
                print("  " + s)
    
def __kline_sharp_day__(stock_dict, date):
    stocks = []
    
    if stock_dict is None or date is None:
        return
    
    for code,stock in stock_dict.items():
        if len(stock) == 0:
            continue
       
        v = stock[date:date]
        if len(v) == 0:
            continue
        
        o = v['open'].values[0]
        c = v['close'].values[0]
        h = v['high'].values[0]
        l = v['low'].values[0]

        if kline_sharp_crossStar(o, c, h, l) and v['ma5_pc'].values[0] < -0.02 and v['v_ma5_pc'].values[0] < 0:
            stocks.append(code)
#             print("  " + code)
    return stocks
            
def kline_sharp_date(path, date):
    stock_dict = sdl.load_path2dict_date(path, date)
    kline_sharp(stock_dict)
                
if __name__ == "__main__":
    stock = sdl.load_file2df("F:/StockData/real/SH#600000.txt")

    for i, v in stock.iterrows():
        o = v['open']
        c = v['close']
        h = v['high']
        l = v['low']

        # print("{} {} {} {} {}".format(i, o, c, h, l), end='')
        if kline_sharp_crossStar(o, c, h, l):
            print(i)