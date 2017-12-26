import numpy as np
import StockKlineSharp as sks
import StockLearningData as sld

def strategy_crossstar_low(stock, idx):
    DOWN_THRESHOLD = 0.1

    cur = stock.iloc[idx]
    o = cur['open']
    c = cur['close']
    h = cur['high']
    l = cur['low']

    # print("{} {} {} {} {}".format(stock.index[idx], o, c, h, l))
    is_crossstar = sks.kline_sharp_crossStar(o, c, h, l)
    if not is_crossstar:
        return False

    trend_start_idx = sld.get_idx_back_trend_end_from_st_ma5_pc(stock, idx)
    begin = stock.iloc[trend_start_idx]
    ma5_start = begin['ma5']
    ma5_end = cur['ma5']

    if ma5_start <= ma5_end:
        return False

    ma5_pc = (ma5_start - ma5_end)/ma5_end

    if ma5_pc < DOWN_THRESHOLD:
        return False

    # print("{} {} {} {} {}".format(stock.index[idx], stock.index[trend_start_idx], ma5_start, ma5_end, ma5_pc))
    return True

def strategy_volume_boost(stock, idx):
    BOOST_THRESHOLD = 10

    trend_start_idx = sld.get_idx_back_trend_end_from_st(stock, idx, 'v_ma10_pc')
    start = stock.iloc[trend_start_idx]['v_ma10']
    end = stock.iloc[idx]['v_ma10']

    if np.isnan(start) or np.isnan(end):
        return False

    if start >= end:
        return False

    v_ma10_pc = (end - start)/start

    if v_ma10_pc < BOOST_THRESHOLD:
        return False

    # print("{} {} {} {} {}".format(stock.index[idx], stock.index[trend_start_idx], start, end, v_ma10_pc))
    return True