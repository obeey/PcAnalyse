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

    trend_start_idx = sld.get_idx_back_trend_end_from_st(stock, idx)
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