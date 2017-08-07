
from StockPattern import *
from functools import reduce
import matplotlib.dates as mdates

class PatternMatch:
    SIM = 75

    def __init__(self):
        # stock_list's type is StockPattern.
        self.stock_list  = []

    def __is_matched(self, to_matched, to_compared):
        sim  = []
        for i in range(StockPattern.PATTERN_LEN - 1):
            start_point = to_matched[i]
            if 0 == start_point:
                start_point = 1
            change  = percentChange(start_point, to_compared[i])
            # print(repr(to_matched[i])+" "+repr(to_compared[i])+ " => " + repr(change))

            sim.append(10000 - abs(change))

        how_sim = (int)(reduce(lambda x, y: x + y, sim) / len(sim))
        # print(how_sim)

        if how_sim >= PatternMatch.SIM*100:
            return True
        else:
            return False

    def get_stock(self, code):
        for stock in self.stock_list:
            if code == stock.stockCode:
                return stock
        return None

    def current_pattern(self, code):
        for stock in self.stock_list:
           if code == stock.stockCode:
               return stock.curPattern

        return None

    """pattern_for_match is a pattern list. (stockCode, (date, pattern, futureOutcome))"""
    def matched_pattern(self, pattern_for_match):
        if None == pattern_for_match:
            return

        matched_pattern_list    = []

        for stock in self.stock_list:
            if None == stock.hisPattern:
                continue

            # print("Match for "+stock.stockCode)
            for pattern in stock.hisPattern:
                if self.__is_matched(pattern_for_match, pattern.patternLst):
                    matched_pattern_list.append((stock.stockCode, pattern))
                    matched_date    = mdates.num2date(pattern.date).strftime("%Y/%m/%d")
                    # print("\t" + stock.stockCode + "\t" + matched_date + "\t" + repr(pattern.futureOutCome))

        return matched_pattern_list

