
from datetime import datetime
from StockItem import *
from StockPattern import *
from PatternMatch import  *
import matplotlib.dates as mdates
import numpy as np
import os
import sys

def load_data(path):
    if os.path.isdir(path) == False:
        print("Not dir")
        return

    pattern_match  = PatternMatch()

    for f in os.listdir(path):
        full_path   = os.path.join(path,f)
        # if False == os.path.isfile(full_path):
        #     continue

        if ('SH' != f[:2]) and ('SZ' != f[:2]):
            continue
        # print(f)

        input_file  = open(full_path)
        lines       = input_file.readlines()
        if (5 + StockPattern.PATTERN_LEN + StockPattern.OUTCOME_RANGE) > len(lines):
            print(f + " 's data is too small. "+repr(len(lines)))
            continue

        lines       = lines[4:-1]
        input_file.close()

        stock_code  = f[3:-4]
        # print("Add " + repr(stock_code) + ". LEN: " + repr(len(lines)))

        date, op, hi, lo, cl, vol, trans = np.loadtxt(lines, unpack=True,
                                         # delimiter='\t',
                                         converters={0: mdates.bytespdate2num('%Y/%m/%d')},
                                         )
        stock_item_list = []
        for i in range(len(date)):
            stock_item_list.append(StockItem(date[i], op[i], hi[i], lo[i], cl[i], vol[i], trans[i]))

        stock_item_list.reverse()
        # print(stock_code + repr(stock_item_list[0]))

        stock_pattern   = StockPattern(stock_code, stock_item_list)
        pattern_match.stock_list.append(stock_pattern)

    return pattern_match

def get_probability(outcome):
    if 0 == len(outcome): return 50

    valid   = [x for x in outcome if 100 < abs(x)]   # future outcome within one percent not considered.
    if 0 == len(valid): return 50

    raise_value = 0
    raise_ctr   = 0
    down_value  = 0
    down_ctr    = 0
    for v in valid:
        if 0 < v:
            raise_value += v
            raise_ctr   += 1
        else:
            down_value  += v
            down_ctr    += 1

    probability_ctr = (raise_ctr*100)/len(valid)
    print("Counter probability is: " + repr(probability_ctr))

    probability_value   = ((raise_value/raise_ctr) + (down_value/down_ctr))/100
    print("Value probability is: " + repr(probability_value))

    probability     = probability_value + probability_ctr
    # print(repr(total_outcome))

    if probability >= 100: probability = 99
    if probability <= 0:    probability = 1

    return probability

def get_output_file_name():
    now = datetime.now()
    return "result_" + now.strftime("%Y-%m-%d_%H-%M") + ".txt"

if __name__ == '__main__':
    output_file_name    = get_output_file_name()
    output_file         = open(output_file_name, 'w')

    # print("Start "+str(datetime.now()))
    output_file.write("Start "+str(datetime.now()))

    if 1 < len(sys.argv):
        input_file_name   = sys.argv[1]
    else:
        input_file_name   = 'F:\project\StockPattern\data\small'

    # pattern_match   = load_data('D:\金长江网上交易\金长江网上交易财智版\T0002\export')
    pattern_match   = load_data(input_file_name)

    print("Load  " + str(datetime.now()))

    for stock_for_match in pattern_match.stock_list:
        # print("Match for "+stock_for_match.stockCode)
        pattern_lst = pattern_match.matched_pattern(stock_for_match.curPattern.patternLst)

        outcome = []
        for code, pattern in pattern_lst:
            outcome.append(pattern.futureOutCome)

        probability = get_probability(outcome)
        print(stock_for_match.stockCode + "\t" + repr(probability) + "%\t" + repr(len(outcome)))

    print("Complete " + str(datetime.now()))
