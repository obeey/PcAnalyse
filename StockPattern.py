
from functools import reduce
from StockPatternItem import *

def percentChange(start_point, current_point):
    try:
        x = ((float(current_point) - start_point) / abs(start_point)) * 100.00
        if x == 0.0:
            return 0.000000001
        else:
            return x
    except:
        return 0.0001

class StockPattern:
    """StockPattern store a stock's pattern."""

    PATTERN_LEN     = 60
    OUTCOME_RANGE   = 5

    def __init__(self, stock_code, stock_item):
        self.stockCode  = stock_code
        # print("\nGet " + stock_code + " current")
        self.curPattern = self.__getCurPattern(stock_item)
        # print("Get " + stock_code + " history")
        self.hisPattern = self.__getHisPattern(stock_item)

    def __getAvg(self, stock):
        return (stock.open + stock.close)/2

    def __getPattern(self, stock_item, start_idx):

        if StockPattern.PATTERN_LEN > len(stock_item):
            return None

        cp  = self.__getAvg (stock_item[start_idx])
        cur_pattern_item  = StockPatternItem()
        cur_pattern_item.date   = stock_item[start_idx].date

        for i in range(1, StockPattern.PATTERN_LEN):
            avg     = self.__getAvg (stock_item[start_idx + i])
            change  = percentChange(cp, avg)
            cur_pattern_item.patternLst.append(change)
            # print(change, end=' ')

        # print()

        if StockPattern.OUTCOME_RANGE <= start_idx:
            sp  = start_idx - StockPattern.OUTCOME_RANGE
            outcome_range_stock = stock_item[sp:start_idx]
            outcome_range   = [self.__getAvg(stock) for stock in outcome_range_stock]
            outcome_value   = reduce(lambda x,y: x+y, outcome_range)/len(outcome_range)
            cur_pattern_item.futureOutCome    = percentChange(cp, outcome_value)

        return cur_pattern_item

    def __getHisPattern(self, stock_item):
        # print("stock item length: " + repr(len(stock_item)))

        if (StockPattern.PATTERN_LEN + StockPattern.OUTCOME_RANGE) > len(stock_item):
            return None

        his_pattern_lst = []

        for i in range(StockPattern.OUTCOME_RANGE, len(stock_item)-StockPattern.PATTERN_LEN):
            his_pattern_lst.append(self.__getPattern(stock_item, i))

        return his_pattern_lst

    def __getCurPattern(self, stock_item):
        return self.__getPattern(stock_item, 0)

