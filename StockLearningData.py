import datetime
import numpy as np
import StockTrend as st
import StockDataLoad as sdl
# import pandas as pd

SLD_HIST_PATTERN_LEN    = 30


def get_predict_item(stock_frame, idx):
    learning_data_item = []

    for i in range(idx + 1 - SLD_HIST_PATTERN_LEN, idx + 1):
        sf = stock_frame.iloc[i]
        learning_data_item.append(sf['close_pc'])
        learning_data_item.append(sf['volume_pc'])
        learning_data_item.append(sf['rise_pc'])
        learning_data_item.append(sf['amplitude'])
        learning_data_item.append(sf['ma5_pc'])
        learning_data_item.append(sf['v_ma5_pc'])

    return learning_data_item


def get_learning_category(stock_frame, idx_start, idx_end):
    start = stock_frame['ma5'][idx_start]
    end = stock_frame['ma5'][idx_end]

    pc = (end - start)*100/start
    category = st.get_trend_category(pc)
    return category


def get_idx_end_from_st(stock_frame, idx):
    trend_length = st.get_trend_stage(stock_frame['ma5_pc'][idx:])
    idx_end = idx + trend_length - 1

    return idx_end


def get_learning_item_from_idx(stock_frame, idx_start, idx_end):
    # learning_target_item = []

    learning_data_item = get_predict_item(stock_frame, idx_start)
    if np.any(np.isnan(learning_data_item)) or np.any(np.isinf(learning_data_item)):
        return None, None

    category = get_learning_category(stock_frame, idx_start, idx_end)

    # print("{} {} {}".format(idx_delta, pc, category))
    # learning_target_item.append(category)

    return learning_data_item, category


def get_learning_item(stock_frame, idx):
    idx_end = get_idx_end_from_st(stock_frame, idx)

    return get_learning_item_from_idx(stock_frame, idx, idx_end)


def preliminary_data(stock_frame):
    stock_open_shift = stock_frame['open'].shift()

    stock_frame['close_pc'] = stock_frame['close'].pct_change()
    stock_frame['volume_pc'] = stock_frame['volume'].pct_change()
    stock_frame['ma5_pc'] = stock_frame['ma5'].pct_change()
    stock_frame['v_ma5_pc'] = stock_frame['v_ma5'].pct_change()
    stock_frame['rise_pc'] = (stock_frame['close'] - stock_open_shift)/stock_open_shift
    stock_frame['amplitude'] = (stock_frame['high'] - stock_frame['low'])/stock_frame['low']


def get_learning_data_from_df(stock_frame):
    stock_len   = len(stock_frame)
    data = []
    target = []

    if stock_len <= SLD_HIST_PATTERN_LEN+1:
        return None, None

    preliminary_data(stock_frame)

    stock_frame = stock_frame.drop(stock_frame.index[0])

    # trend_end = 0
    # i is the current index for predict
    # for i in range(SLD_HIST_PATTERN_LEN - 1, stock_len - 3):
    #     if i >= trend_end:
    #         trend_end = get_idx_end_from_st(stock_frame, i)
    i = SLD_HIST_PATTERN_LEN - 1
    while i < stock_len - 3:
        # print(stock_frame.index[i])
        trend_end = get_idx_end_from_st(stock_frame, i)
        data_item, target_item = get_learning_item_from_idx(stock_frame, i, trend_end)
        i = trend_end
        if data_item is None or target_item is None:
            continue

        data.append(data_item)
        target.append(target_item)

    return data, target


def get_learning_data_from_dict_idx(stock_dict, idx):
    if stock_dict is None:
        return None, None

    data = []
    target = []

    stock_nums = len(stock_dict)
    sn = 0

    for k, v in stock_dict.items():
        sn += 1

        if 0 == sn % 100:
            print("{}/{}".format(sn, stock_nums))

        if 15 >= len(v):
            continue

        d, t = get_learning_data_from_df(v.drop(v.index[range(idx)]))
        if d is None or v is None:
            continue

        # The first include None element. The last elements not a complete trend.
        data.extend(d[1:-10])
        target.extend(t[1:-10])

    return data, target



def get_learning_data_from_dict(stock_dict):
    return get_learning_data_from_dict_idx(stock_dict, 4)


def get_idx_from_df(df, date):
    if df is None:
        return 0

    idx_date = datetime.datetime.strptime(date,  "%Y/%m/%d")

    start_date = datetime.datetime.strptime(df.index[0], "%Y/%m/%d")
    end_date = datetime.datetime.strptime(df.index[len(df) - 1], "%Y/%m/%d")

    if idx_date <= start_date:
        return 0

    if idx_date >= end_date:
        return len(df) - 1

    one_day = datetime.timedelta(1)

    while idx_date < end_date:
        try:
            idx = df.index.get_loc(date)
            return idx
        except KeyError:
            idx_date = idx_date + one_day
            date = idx_date.strftime("%Y/%m/%d")
            continue

    return len(df) - 1


def reshape_df(df, start_date, end_date=None):
    length = len(df)
    idx_start = 0

    if start_date is not None:
        idx_start = get_idx_from_df(df, start_date)

        if idx_start > 0:
            length = length - idx_start - 1
            if 15 >= length:
                return df

    if end_date is not None:
        idx_end = get_idx_from_df(df, end_date)
        if idx_end < len(df)-1:
            if 15 >= length - (len(df)-idx_end-1):
                return df
            else:
                df = df.drop(df.index[range(idx_end, len(df))])

    if start_date is not None and idx_start > 0:
        df = df.drop(df.index[range(idx_start)])

    return df


def get_learning_data_from_dict_date(stock_dict, start_date, end_date=None):
    if stock_dict is None:
        return None, None

    data = []
    target = []

    stock_nums = len(stock_dict)
    sn = 0

    for k, v in stock_dict.items():
        sn += 1

        if 0 == sn % 100:
            print("{}/{}".format(sn, stock_nums))

        if 45 >= len(v):
            continue

        v = reshape_df(v, start_date, end_date)
        d, t = get_learning_data_from_df(v)
        if d is None or v is None:
            continue

        # The first include None element. The last elements not a complete trend.
        data.extend(d[1:-10])
        target.extend(t[1:-10])

    return data, target


def get_learning_data_from_path(path):
    stock_dict = sdl.load_path2dict(path)

    return get_learning_data_from_dict(stock_dict)
