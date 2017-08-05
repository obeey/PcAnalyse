
from StockPattern import *
from functools import reduce
import matplotlib.dates as mdates

class PatternMatch:
    SIM = 85

    def __init__(self):
        # stock_list's type is StockPattern.
        self.stock_list  = []

    def __is_matched(self, to_matched, to_compared):
        sim  = []
        for i in range(StockPattern.PATTERN_LEN - 1):
            start_point = to_matched[i]
            if 0.0 == start_point:
                start_point = 0.000001
            change  = percentChange(start_point, to_compared[i])
            # print(repr(to_matched[i])+" "+repr(to_compared[i])+ " => " + repr(change))

            sim.append(100.00 - abs(change))

        how_sim = reduce(lambda x, y: x + y, sim) / len(sim)
        # print(how_sim)

        if how_sim >= PatternMatch.SIM:
            return True
        else:
            return False

    def current_pattern(self, code):
        for stock in self.stock_list:
           if code == stock.stockCode:
               return stock.curPattern

        return None

    """pattern_for_match is a pattern list. (stockCode, (date, pattern, futureOutcome))"""
    def matched_pattern(self, pattern_for_match):
        matched_pattern_list    = []

        for stock in self.stock_list:
            if None == stock.hisPattern:
                continue

            # print("Match for "+stock.stockCode)
            for pattern in stock.hisPattern:
                if self.__is_matched(pattern_for_match, pattern.patternLst):
                    matched_pattern_list.append((stock.stockCode, pattern))
                    # print("\t" + stock.stockCode + "\t" + repr(pattern.futureOutCome))

        return matched_pattern_list

