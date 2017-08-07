
from functools import reduce
from StockPatternItem import *

def percentChange(start_point, current_point):
    try:
        x = ((current_point - start_point)*10000) // abs(start_point)
        if x == 0:
            return 1
        else:
            return x
    except:
        return 1

class StockPattern:
    """StockPattern store a stock's pattern."""

    PATTERN_LEN     = 30
    OUTCOME_RANGE   = 10

    MA5_RANGE       = 5

    def __init__(self, stock_code, stock_item_list):
        self.stockCode  = stock_code

        self.__calc_ma5(stock_item_list)

        # print("\nGet " + stock_code + " current")
        self.curPattern = self.__get_cur_pattern(stock_item_list)
        # print("Get " + stock_code + " history")
        self.hisPattern = self.__get_his_pattern(stock_item_list)

    def __calc_ma5(self, stock_item_list):
        if StockPattern.MA5_RANGE > len(stock_item_list): return

        for i in range(len(stock_item_list) - StockPattern.MA5_RANGE + 1):
            stock_item_list[i].ma5   = 0
            for item in stock_item_list[i:i+StockPattern.MA5_RANGE]:
                stock_item_list[i].ma5   += self.__get_avg(item)

            stock_item_list[i].ma5  //= StockPattern.MA5_RANGE

    def __get_avg(self, stock_item):
        return (stock_item.open + stock_item.close) // 2

    def __get_ma5(self, stock_item):
        return stock_item.ma5

    def __get_pattern(self, stock_item_list, start_idx, get_value):

        if StockPattern.PATTERN_LEN > len(stock_item_list):
            return None

        # cp  = self.__get_avg (stock_item[start_idx])
        cp  = get_value(stock_item_list[start_idx])
        if None == cp: return

        cur_pattern_item  = StockPatternItem()
        cur_pattern_item.date   = stock_item_list[start_idx].date

        for i in range(1, StockPattern.PATTERN_LEN):
            # avg     = self.__get_avg (stock_item[start_idx + i])
            avg     = get_value(stock_item_list[start_idx + i])
            if None == avg: return
            change  = percentChange(cp, avg)
            cur_pattern_item.patternLst.append(change)
            # print(change, end=' ')

        # print()

        if StockPattern.OUTCOME_RANGE <= start_idx:
            sp  = start_idx - StockPattern.OUTCOME_RANGE
            # outcome_range_stock = stock_item_list[sp:start_idx]
            # outcome_range   = [self.__get_avg(stock) for stock in outcome_range_stock]
            # outcome_value   = int(reduce(lambda x,y: x+y, outcome_range)/len(outcome_range))
            outcome_value   = stock_item_list[sp].ma5
            cur_pattern_item.futureOutCome    = percentChange(cp, outcome_value)
            # print("outcome " + repr(cur_pattern_item.futureOutCome) + '\t' + repr(cp) + '\t' + repr(outcome_value))

        return cur_pattern_item

    def __get_his_pattern(self, stock_item_list):
        # print("stock item length: " + repr(len(stock_item)))

        if (StockPattern.PATTERN_LEN + StockPattern.OUTCOME_RANGE) > len(stock_item_list):
            return None

        his_pattern_lst = []

        for i in range(StockPattern.OUTCOME_RANGE, len(stock_item_list)-StockPattern.PATTERN_LEN):
            pattern = self.__get_pattern(stock_item_list, i, self.__get_ma5)
            if None == pattern: break

            his_pattern_lst.append(pattern)

        return his_pattern_lst

    def __get_cur_pattern(self, stock_item_list):
        return self.__get_pattern(stock_item_list, 0, self.__get_ma5)

