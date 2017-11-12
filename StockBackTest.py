import datetime
import StockStrategy as ss

def backtest_sigle_stock(stock_df):
    date_lst = []
    for idx in range(len(stock_df)-1,10,-1):
        if ss.strategy_crossstar_low(stock_df, idx):
            date_str = stock_df.index[idx]
            date_lst.append(date_str)

            print(date_str)

    return date_lst


def backtest_all_stock_specify_date(stock_dict, date_str):
    for c,v in stock_dict.items():
        try:
            idx = v.index.get_loc(date_str)
        except KeyError:
            continue

        # print(idx)
        if ss.strategy_crossstar_low(v, idx):
            print("\t"+c)


def backtest_all_stock_range_date(stock_dict, date_str_begin, date_str_end=None):
    if date_str_end:
        date_end = datetime.datetime.strptime(date_str_end, "%Y/%m/%d")
    else:
        date_end = datetime.datetime.today()

    date_cur = datetime.datetime.strptime(date_str_begin, "%Y/%m/%d")
    oneday = datetime.timedelta(1)

    while date_cur <= date_end:
        cur_date_str = date_cur.strftime("%Y/%m/%d")
        print(cur_date_str)
        backtestr_all_stock_specify_date(stock_dict, cur_date_str)

        date_cur += oneday