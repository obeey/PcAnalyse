import datetime
import numpy as np
import pandas as pd
import tensorflow       as tf
import StockLearningData as sld
import StockDataLoad as sdl
import StockKlineSharp as sks

def get_predict_data(k, date):
#     k = ts.get_hist_data(c, start=start_date, end=end_date)

    if k is None or (sld.SLD_HIST_PATTERN_LEN + 5) > len(k):
#         print(code + " too small.")
        return None
        
    #k = k.iloc[::-1]

#     sld.preliminary_data(k)

    try:
        idx = k.index.get_loc(date)
    except KeyError:
#         print("{} {} not found.".format(code, date))
        return None
    
#     k_predict = sld.get_predict_item(k, idx)
    k_predict = sld.get_normalize_predict_item(k, idx)
    if k_predict is None:
        return None
    
    return k_predict


def predict_estimator(classifier, predicted_list, code_list):
    """
    predict_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": np.array(predicted_list)},
      num_epochs=1,
      shuffle=False)
    
    predictions = list(classifier.predict(input_fn=predict_input_fn))

#     predicted_classes = int(predictions[0]["classes"][0])
#     predicted_probability = predictions[0]['probabilities'][predicted_classes]
    # print("  {} {} {} {}".format(code, date, predicted_classes, predicted_probability))
    
#     return predictions, code_list
    print(predictions)

    result = [[code_list[idx], int(r["classes"]), r['probabilities'][int(r["classes"])]] for idx, r in enumerate(predictions)]

#     result = [x for x in result if x[2] > 0.8]
    """
#     print(predicted_list)
    predictions = list(classifier.predict_proba(np.array(predicted_list)))
#     print(predictions)

    result = [[code_list[idx], 0 if r[0] > r[1] else 1, r[0] if r[0] > r[1] else r [1]] for idx, r in enumerate(predictions)]
    return result

def predict_keras(model, predicted_list, code_list):
        predictions = model.predict(np.array(predicted_list))
        # result = [[code_list[idx], 0, np.where(r == 1)[0][0]] for idx,r in enumerate(predictions) if r[0] != np.nan]
        result = [[code_list[idx], 0, np.where(r == 1)[0]] for idx,r in enumerate(predictions) if not np.isnan(r).any()]
        result = [[r[0],r[1],r[2][0] if r[2] != [] else 2] for idx, r in enumerate(result)]
        # print(predicted_list[0])
        # print(result)

        return result

def get_predicted_df(classifier, stock_dict_original, stock_dict_normal, date):
    predicted_list = []
    code_list = []

    for c, v in stock_dict_normal.items():
        stock_predicted = get_predict_data(v, date)
        if stock_predicted is not None:
            predicted_list.append(stock_predicted)
            code_list.append(c)

    if 0 == len(predicted_list):
        # print("No data for predict.")
        return None
    
    result = predict_estimator(classifier, predicted_list, code_list)
#     result = predict_keras(classifier, predicted_list, code_list)

    for x in result:
        k = stock_dict_original[x[0]]
        si = k.index.get_loc(date)
        ei = sld.get_idx_trend_end_from_st(k, si)
        x.append(sld.get_learning_range_pc(k, si, ei))    
                 
#     cat = [p.insert(0, c) for c, p in zip(code_list, result)]
    predicted_df = pd.DataFrame(result, columns=['code', 'class', 'probability', 'pc']) 
    return predicted_df


def predict_stock_range(classifier, stock_dict, date_start, date_end):
    if date_start is None or date_end is None:
        print("Please provide the date range.")
        return
    
#     for c, v in stock_dict.items():
#         sl.preliminary_data(v)
        
    start = datetime.datetime.strptime(date_start, '%Y/%m/%d')
    end = datetime.datetime.strptime(date_end, '%Y/%m/%d')
    
    one_day = datetime.timedelta(1)
    
    stock_dict_origin = {}
    for c,v in stock_dict.items():
        stock = v.dropna()
        if len(stock) >= sld.SLD_HIST_PATTERN_LEN:
            stock_dict_origin[c] = stock

    stock_dict_normal = sdl.load_normalization_from_dict(stock_dict_origin)
    while start <= end:
        weekday = start.isoweekday()
        if 6 == weekday or 7 == weekday:
            start += one_day
            continue
            
        day_for_predicted = start.strftime('%Y/%m/%d')
        # print(day_for_predicted)
        predict_stock_day(classifier, stock_dict_origin, stock_dict_normal, day_for_predicted)
        
        start += one_day
#         df = get_predicted_df(classifier, stock_dict, day_for_predicted)
#         if df is None:
#             continue
            
# #         raise_df = df[df['class'] >= 4]
# #         raise_df = raise_df[raise_df['probability'] > 0.8]
        
# #         down_df = df[df['class'] <= 2]
# #         down_df = down_df[down_df['probability'] > 0.8]
# #         if 0 == len(raise_df) and 0 == len(down_df):
# #             continue

# #         df = df[df['probability'] > 0.8]
#         if 0 == len(df):
#             continue
        
#         class_one = len(df[df['class'] == 1])
#         rate = class_one/len(df)
#         print("\n{} {}\t{}".format(day_for_predicted, 'up' if rate > 0.8 else 'fall', rate))
# #         print();print("{}\t{}".format(day_for_predicted, class_one/len(df)))
#         for idx, row in df.iterrows():
#             if row['probability'] > 0.999 :
#                 print("{} {} {} {}".format(row['code'], row['class'], row['probability'], row['pc']))



    
# #         for idx, row in raise_df.iterrows():
# #             print("{} {} {}".format(row['code'], row['class'], row['probability']))
            
# #         for idx, row in down_df.iterrows():
# #             print("{} {} {}".format(row['code'], row['class'], row['probability']))

def predict_stock_today(classifier, stock_dict):
    today = datetime.datetime.today()
    today_str = today.strftime('%Y/%m/%d')
#     predict_stock_range(classifier, stock_dict, today_str, today_str)
    predict_stock_day(classifier, stock_dict, sdl.load_normalization_from_dict(stock_dict), today_str)


def predict_stock_day(classifier, stock_dict_original, stock_dict_normal, date_str, code=None):
    if date_str is None:
        print("Please provide the date range.")
        return
    
#     for c, v in stock_dict.items():
#         sld.preliminary_data(v)

    day_for_predicted = date_str
#         print(day_for_predicted)

    df = get_predicted_df(classifier, stock_dict_original, stock_dict_normal, day_for_predicted)
    if df is None or 0 == len(df):
        return

    """ 
    class_one = len(df[df['class'] == 1])
#     class_one = len(df[df['class'] == 3 or df['class'] == 4])
    rate = class_one/len(df)
    print("{}-{}-{}".format(day_for_predicted, 'U' if rate > 0.8 else 'D', rate))
    """
    print(day_for_predicted)

    if code is not None:
        df = df[df['code'] == code]

    for idx, row in df.iterrows():
        # if row['probability'] > 0.999 and row['class'] == 1 and row['pc'] > 30 :
        # if  (row['class'] == 1) and (row['probability'] > 0.6):
        if  (row['class'] == 1) :
            print("  {} {} {}\t {}".format(row['code'], row['class'], row['probability'], row['pc']))

def predict_result_show_print(stock_dict, date, codes):
    if len(codes) <= 0:
        return
    
    print(date)
    for c in codes:
        print("  "+c)

import matplotlib.pyplot as plt
# plt.xticks(rotation=90)

def predict_result_show_graph(stock_dict, date, codes):
    COLUMNS = 2
    subs = len(codes)
    rows = (subs+COLUMNS-1)//COLUMNS
    
    fig, axs = plt.subplots(rows, COLUMNS, figsize=(15, 10), squeeze=False)
    
    for i in range(subs):
        c = codes[i]
        stock = stock_dict[c][date + datetime.timedelta(days=1):date + datetime.timedelta(days=21)]['close']
        ax = axs[i//COLUMNS][i % COLUMNS]
        ax.set_title(c)
        ax.plot(stock)
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)
    fig.suptitle(date)
#     fig.show()
    
def __predict_day__(stock_dict, actions, date):
    selects = []
    idx = 0
    
    for code,stock in stock_dict.items():
        if len(stock) == 0:
            continue

        try:
            idx = stock.index.get_loc(date)
        except KeyError:
            continue

        for action in actions:
            result = action(stock, idx)
            if result:
                selects.append(code)
                break
                
    return selects
                    
def predict_day(stock_dict, actions, date_str):
    ds = date_str.split('/')
    date = datetime.date(int(ds[0]), int(ds[1]), int(ds[2]))
    
    return __predict_day__(stock_dict, actions, date)

def predict_range(stock_dict, actions, start_str=None, end_str=None, show_action=predict_result_show_print):
#     start_date
#     end_date
    if start_str is None:
        start_str = '1997/04/30'
#     start = datetime.strptime(start_str, '%Y/%m/%d')
    if end_str is None:
        end_date = datetime.date.today()
    else:
        ds = end_str.split('/')
        end_date = datetime.date(int(ds[0]), int(ds[1]), int(ds[2]))
        
    ds = start_str.split('/')
    start_date = datetime.date(int(ds[0]), int(ds[1]), int(ds[2]))
        
    dates = pd.bdate_range(start_date, end_date).tolist()
    for d in dates:
        selects = __predict_day__(stock_dict, actions, d)
        if len(selects) > 0:
            show_action(stock_dict, d, selects)
                
def predict_kline_sharp_action(stock_df, idx):
    r = stock_df.iloc[idx]
    
    o = r['open']
    c = r['close']
    h = r['high']
    l = r['low']
    
    return True if sks.kline_sharp_crossStar(o, c, h, l) and r['ma5_pc'] < -0.02 and r['v_ma5_pc'] < -0.02 else False

def predict_continuous_fall_action(stock_df, idx):
    CONTINUOUS_LEN = 5
    AMPLITUDE = 0.3
    
    if idx < CONTINUOUS_LEN+1:
        return False
    
    p = stock_df.iloc[idx-CONTINUOUS_LEN]
    r = stock_df.iloc[idx]
    
    o = p['close']
    c = r['close']
    if (o - c)/o < AMPLITUDE:
        return False
    
#     p = stock_df.iloc[idx-1]
    r = stock_df.iloc[idx]
    
    o = r['open']
    c = r['close']
    
    if c <= o:
        return False
    
    for i in range(idx - CONTINUOUS_LEN, idx):
        p = stock_df.iloc[i-1]
        r = stock_df.iloc[i]
    
        o = p['close']
        c = r['close']
        
        if c > o:
            return False
        
    return True