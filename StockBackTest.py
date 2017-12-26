import datetime
import matplotlib.pyplot as plt
import matplotlib.dates  as mdates
import StockStrategy as ss

def backtest_sigle_stock(stock_df):
    date_lst = []
    for idx in range(len(stock_df)-1,10,-1):
        # if ss.strategy_crossstar_low(stock_df, idx):
        if ss.strategy_volume_boost(stock_df, idx):
            date_str = stock_df.index[idx]
            date_lst.append(date_str)

            print(date_str)

    return date_lst

def backtest_stock_show(stock_lst, date_str):
    COLS = 5
    RANGE = 100
    stock_num = len(stock_lst)
    if stock_num == 0:
        return

    lines = (stock_num + COLS - 1)//COLS

    # fig = plt.figure()
    
    fig, ax_lst = plt.subplots(lines, COLS)
    # fig.clear()
    fig.suptitle(date_str)

    for i in range(stock_num):

        # ax = fig.add_subplot(lines, COLS, i+1)
        x = i//COLS
        y = i % COLS
        # print("{} {}".format(x, y))
        if stock_num <= COLS:
            ax = ax_lst[i]
        else:
            ax = ax_lst[x, y]
        # ax.cla()

        # if i >= stock_num:
        #     ax.plot(0,0)
        #     continue

        # ax.xaxis_date()
        # fmt = mdates.DateFormatter("%Y/%m%d")
        # ax.xaxis.set_major_formatter(fmt)

        code, stock, idx = stock_lst[i]
        feature = stock['close']
        # ax.plot(feature[idx - RANGE: idx + RANGE + 1], 'b-')

        # if len(feature) < RANGE*2 + 1:
        #     continue

        feature = feature[idx - RANGE: idx + RANGE + 1]
        if len(feature) == 0:
            continue

        feature.plot(style='b-', ax=ax, rot=45)
        # feature[idx].plot(style='ro', ax=ax)
        # ax.plot(mdates.date2num(datetime.datetime.strptime(date_str, '%Y/%m/%d')), feature[idx], 'ro')
        ax.set_title(code)

    plt.show()


# strategy : ss.strategy_volume_boost
def backtest_all_stock_specify_date(stock_dict, strategy, date_str):
    stock_lst = []

    for c, v in stock_dict.items():
        try:
            idx = v.index.get_loc(date_str)
        except KeyError:
            continue

        # print(idx)
        # if ss.strategy_crossstar_low(v, idx):
        if strategy(v, idx):
            stock_lst.append((c, v, idx))
            print("\t"+c)

    # backtest_stock_show(stock_lst, date_str)
    return stock_lst

def backtest_all_stock_range_date(stock_dict, strategy, date_str_begin, date_str_end=None):
    if date_str_end:
        date_end = datetime.datetime.strptime(date_str_end, "%Y/%m/%d")
    else:
        date_end = datetime.datetime.today()

    date_cur = datetime.datetime.strptime(date_str_begin, "%Y/%m/%d")
    oneday = datetime.timedelta(1)

    while date_cur <= date_end:
        cur_date_str = date_cur.strftime("%Y/%m/%d")
        print(cur_date_str)
        stock_lst = backtest_all_stock_specify_date(stock_dict, strategy, cur_date_str)
        # backtest_stock_show(stock_lst, cur_date_str)

        date_cur += oneday
