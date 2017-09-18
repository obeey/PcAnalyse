import StockTrend as st
import pandas as pd

SLD_HIST_PATTERN_LEN    = 30


def get_predict_item(stock_frame, idx):
    learning_data_item = []

    for i in range(idx + 1 - SLD_HIST_PATTERN_LEN, idx + 1):
        learning_data_item.append(stock_frame.iloc[i]['close_pc'])
        learning_data_item.append(stock_frame.iloc[i]['volumn_pc'])
        learning_data_item.append(stock_frame.iloc[i]['rise_pc'])
        learning_data_item.append(stock_frame.iloc[i]['amplitude'])
        learning_data_item.append(stock_frame.iloc[i]['ma5_pc'])
        learning_data_item.append(stock_frame.iloc[i]['v_ma5_pc'])

    return learning_data_item


def get_learning_item(stock_frame, idx):
    learning_target_item = []

    learning_data_item = get_predict_item(stock_frame, idx)

    idx, pc = st.get_trend_stage(stock_frame['ma5'][idx:])
    category = st.get_trend_category(pc)

    # print("{} {} {}".format(idx, pc, category))
    learning_target_item.append(category)

    return learning_data_item, learning_target_item


def preliminary_date(stock_frame):
    stock_open_shift = stock_frame['open'].shift()

    stock_frame['close_pc'] = stock_frame['close'].pct_change()
    stock_frame['volumn_pc'] = stock_frame['volumn'].pct_change()
    stock_frame['ma5_pc'] = stock_frame['ma5'].pct_change()
    stock_frame['v_ma5_pc'] = stock_frame['v_ma5'].pct_change()
    stock_frame['rise_pc'] = (stock_frame['close'] - stock_open_shift)/stock_open_shift
    stock_frame['amplitude'] = (stock_frame['high'] - stock_frame['low'])/stock_frame['low']


def get_learning_data(stock_frame):
    stock_len   = len(stock_frame)
    data = []
    target = []

    if stock_len <= SLD_HIST_PATTERN_LEN:
        return None

    preliminary_date(stock_frame)

    # i is the current index for predict
    for i in range(SLD_HIST_PATTERN_LEN - 1, stock_len - 2):
        data_item, target_item = get_learning_item(stock_frame, i)
        data.append(data_item)
        target.append(target_item)

    return data, target
