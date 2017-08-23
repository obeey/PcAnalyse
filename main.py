
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

    # pattern_match  = PatternMatch()
    pattern_match  = {}

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

        # lines   = lines[:-10]   # back two weeks

        stock_code  = f[3:-4]
        # print("Add " + repr(stock_code) + ". LEN: " + repr(len(lines)))

        date, op, hi, lo, cl, vol, trans = np.loadtxt(lines, unpack=True,
                                         # delimiter='\t',
                                         converters={0: mdates.bytespdate2num('%Y/%m/%d')},
                                         )
        stock_item_list = []
        for i in range(len(date)):
            stock_item_list.append(StockItem(date[i], op[i], hi[i], lo[i], cl[i], vol[i], trans[i]))

        # stock_item_list.reverse()
        # print(stock_code + repr(stock_item_list[0]))

        # stock_pattern   = StockPattern(stock_code, stock_item_list)
        # pattern_match.stock_list.append(stock_pattern)

        pattern_match[stock_code]   = stock_item_list
        # print("Add "+stock_code)
    return pattern_match

def get_probability(outcome):
    # if 0 == len(outcome): return 50

    valid   = [x for x in outcome if 100 < abs(x)]   # future outcome within one percent not considered.
    if 0 == len(valid): return 50,0,0,0

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

    probability_ctr = (raise_ctr*100)//len(valid)
    print("Counter probability is: " + repr(probability_ctr))

    probability_value   = 0
    if 0 != raise_ctr:
        probability_value   = (raise_value//raise_ctr)

    if 0 != down_ctr:
        probability_value   += (down_value//down_ctr)
    probability_value   //= 100
    print("Value probability is: " + repr(probability_value))

    # probability     = probability_value + probability_ctr
    # print(repr(total_outcome))

    # if probability >= 100: probability = 99
    # if probability <= 0:    probability = 1

    return probability_ctr,probability_value,max(outcome)//100,min(outcome)//100

def get_output_file_name():
    now = datetime.now()
    return "result_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"


def match_for_all(output_file, pattern_match):
    for stock_for_match in pattern_match.stock_list:
        # print("Match for "+stock_for_match.stockCode)
        match_for_code(output_file, pattern_match, stock_for_match)


def match_for_code(output_file, pattern_match, stock_for_match):
    pattern_lst = pattern_match.matched_pattern(stock_for_match.curPattern.patternLst)
    outcome = []
    for code, pattern in pattern_lst:
        outcome.append(pattern.futureOutCome)

    probability, avg_v, max_v, min_v = get_probability(outcome)

    code_date   = mdates.num2date(stock_for_match.curPattern.date).strftime("%Y-%m-%d")
    result  = stock_for_match.stockCode + "\t" + code_date + "\t" + repr(len(outcome)) + "\t" + repr(probability) + "%\t"  + repr(avg_v) + "%\t" + repr(max_v) + "%\t" + repr(min_v) + "%"
    print(result)
    output_file.write(result+'\r\n')


def get_volume_hi_price_lo(stock_code, history):
    o   = history[0]
    for i in range(1, len(history)):
        n   = history[i]
        if n.open >= n.close or n.close <= o.close:
            o = n
            continue

        price_change    = percentChange(o.close, n.close)
        volume_change   = percentChange(o.volume, n.volume)

        if price_change < 300 and volume_change > 8000:
            code_date   = mdates.num2date(n.date).strftime("%Y-%m-%d")
            # print("\t"+code_date+"\t" + repr(price_change) +"\t\t" + repr(volume_change) +"\t\t"+ repr(n.close))
            print("\t{}\t {:<8} {:<8} {}".format(code_date, price_change, volume_change,n.close))

            # old_date = mdates.num2date(o.date).strftime("%Y-%m-%d")
            # print("\t{}\tclose [{:<8}{:<8}] volume [{:<12}{:<12}]".format(old_date, o.close, n.close, o.volume, n.volume))

        o   = n

def match_volume_price(stock_list):
    for code, data_lst in stock_list.items():
        print(code)
        get_volume_hi_price_lo(code, data_lst)

if __name__ == '__main__':
    """
    output_file_name    = get_output_file_name()
    output_file         = open(output_file_name, 'w')

    print("Start "+str(datetime.now()))
    output_file.write("Start "+str(datetime.now()) + '\r\n')

    """
    arg_len = len(sys.argv)

    stock_code  = None
    if 2 < arg_len:
        stock_code  = sys.argv[2]

    if 1 < arg_len:
        input_file_name   = sys.argv[1]
    else:
        input_file_name   = 'F:\project\StockPattern\data\small'

    # pattern_match   = load_data('D:\金长江网上交易\金长江网上交易财智版\T0002\export')
    pattern_match   = load_data(input_file_name)

    match_volume_price(pattern_match)

'''
    print("Load  " + str(datetime.now()))
    output_file.write("Load  " + str(datetime.now()) + '\r\n')

    if None == stock_code:
        match_for_all(output_file, pattern_match)
    else:
        print("match for "+stock_code)
        stock   = pattern_match.get_stock(stock_code)
        if None != stock:
            match_for_code(output_file, pattern_match, stock)
        else:
            print("Not found")

    print("Complete " + str(datetime.now()))
    output_file.write("Complete " + str(datetime.now()) + '\r\n')
    output_file.close()
'''
