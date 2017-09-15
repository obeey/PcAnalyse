import StateMachine as sm


def __stock_trend_equal__(a, b):
    return a == b


def __stock_trend_large__(a, b):
    return a > b


def __stock_trend_small__(a, b):
    return a < b


def __stock_trend_change__(cargo, operator):
    idx         = cargo[0]
    pc          = cargo[1]
    idx_max     = len(pc) - 1

    # if 0 == len(pc):
    #     return 'END', cargo

    while idx <= idx_max and operator(0, pc[idx]):
        idx = idx + 1

    return idx


def __stock_trend_start__(cargo):
    pc          = cargo[1]
    idx_max     = len(pc) - 1

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
    return __stock_trend_rd_gen__(cargo,  __stock_trend_large__)


def __stock_trend_down__(cargo):
    return __stock_trend_rd_gen__(cargo,  __stock_trend_small__)


def __stock_trend_end(cargo):
    pass

'''
input:
    stock : Series. It's MA5 for stock normally.
output:
    The end index and the change percent of the stock
'''


def get_trend(stock):
    percent_change = stock.pct_change()

    m = sm.StateMachine()
    m.add_state('START', __stock_trend_start__)
    m.add_state('RAISE', __stock_trend_raise__)
    m.add_state('DOWN', __stock_trend_down__)
    m.add_state('END', __stock_trend_end, end_state=1)

    m.set_start('START')
    cargo = m.run([1, percent_change])

    end_idx = cargo[0]
    return end_idx, (stock[end_idx] - stock[0])/stock[0]