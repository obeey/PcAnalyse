
def kline_sharp_crossStar(open, close, high, low):
    OCPC_THRELDHOLD = 0.001
    OLPC_THRELDHOLD = 0.005
    AR_THRELDHOLD = 3

    if 0 == open:
        return False

    ocpc = abs(close - open)/open
    olpc = abs(open - low )/open

    # print("\t{}\t{}".format(ocpc, olpc))

    if 0 == ocpc:
        if olpc > OLPC_THRELDHOLD:
            return True
        else:
            return False

    amplitude_rate = olpc/ocpc

    if ocpc < OCPC_THRELDHOLD and amplitude_rate > AR_THRELDHOLD:
        return True

    return False

import StockDataLoad as sdl

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