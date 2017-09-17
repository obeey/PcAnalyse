import StateMachine as sm
import pandas as pd

def __stock_trend_equal__(a, b):
    # print("equal {} {}".format(a,b))
    return a == b


def __stock_trend_large__(a, b):
    # print("large {} {}".format(a,b))
    return a > b


def __stock_trend_small__(a, b):
    # print("small {} {}".format(a,b))
    return a < b


def __stock_trend_change__(cargo, operator):
    idx         = cargo[0]
    pc          = cargo[1]
    idx_max     = len(pc) - 1

    if len(pc) == 0:
        return 0

    while (idx <= idx_max and pd.np.isnan(pc[idx])) or (idx <= idx_max and operator(pc[idx], 0)):
        # print("EXECUTE {} {} {} {}".format(idx, idx_max, pc[idx], operator(pc[idx], 0)))
        idx += 1

    # print("return {} {}".format(idx, pc[idx]))
    return idx


def __stock_trend_start__(cargo):
    pc          = cargo[1]
    idx_max     = len(pc) - 1

    # print("START {}".format(cargo[0]))

    idx = __stock_trend_change__(cargo, __stock_trend_equal__)

    if idx > idx_max:
        return 'END', [idx_max, pc]

    if 0 < pc[idx]:
        return 'RAISE', [idx, pc]
    else:
        return 'DOWN', [idx, pc]


def __stock_trend_rd_gen__(cargo, operator):
    pc          = cargo[1]
    idx_max     = len(pc) - 1

    idx = __stock_trend_change__(cargo, operator)

    return 'END', [min(idx, idx_max), pc]


def __stock_trend_raise__(cargo):
    # print("RAISE {}".format(cargo[0]))

    return __stock_trend_rd_gen__(cargo,  __stock_trend_large__)


def __stock_trend_down__(cargo):
    # print("DOWN ".format(cargo[0]))

    return __stock_trend_rd_gen__(cargo,  __stock_trend_small__)


def __stock_trend_end(cargo):
    pass

'''
input:
    stock : Series. It's MA5 for stock normally.
output:
    The end index and the change percent of the stock
'''


def get_trend_stage(stock):
    percent_change = stock.pct_change()

    m = sm.StateMachine()
    m.add_state('START', __stock_trend_start__)
    m.add_state('RAISE', __stock_trend_raise__)
    m.add_state('DOWN', __stock_trend_down__)
    m.add_state('END', __stock_trend_end, end_state=1)

    m.set_start('START')
    cargo = m.run([1, percent_change])

    end_idx = cargo[0]

    # print("index {} start {} end {}".format(end_idx, stock[0], stock[end_idx]))

    return end_idx, (stock[end_idx] - stock[0])/stock[0]

def get_trend_list(stock):
    trend_list  = []
    idx         = 0

    while idx < len(stock)- 1:
        idx_delta, pc = get_trend_stage(stock[idx:])

        print(stock.index[idx] + " index {} delta {} PC {}%".format(idx, idx_delta, pc*100))
        trend_list.append((idx, pc))

        idx += idx_delta

    return trend_list

"""
Category:
    -5  : -20   >   PC
    -4  : -15   >=  PC  > -20
    -3  : -10   >=  PC  > -15
    -2  : -5    >=  PC  >  -10
    -1  : -1    >=  PC  >   -5
    0   : -1    <   PC  < 1
    1   : 1     <=  PC  < 5
    2   : 5     <=  PC  < 10
    3   : 10    <=  PC  < 15
    4   : 15    <=  PC  < 20
    5   : 20    <=  PC
"""
def get_trend_category(pc):
    category_map    = {
        -5  : lambda pc: -20    >   pc,
        -4  : lambda pc: -15    >=  pc  >   -20,
        -3  : lambda pc: -10    >=  pc  >   -15,
        -2  : lambda pc: -5     >=  pc  >   -10,
        -1  : lambda pc: -1     >=  pc  >   -5,
        1   : lambda pc: 1      <=  pc  <   5,
        2   : lambda pc: 5      <=  pc  <   10,
        3   : lambda pc: 10     <=  pc  <   15,
        4   : lambda pc: 15     <=  pc  <   20,
        5   : lambda pc: 20     <=  pc
    }

    for k,v in category_map.items():
        if v(pc):
            return k

    return 0