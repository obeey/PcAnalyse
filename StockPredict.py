import datetime
import numpy as np
import pandas as pd
import StockLearningData as sld
import tensorflow       as tf

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
    
    k_predict = sld.get_predict_item(k, idx)
    
    return k_predict


def get_predicted_df(classifier, stock_dict, date):
    predicted_list = []
    code_list = []

    for c, v in stock_dict.items():
        stock_predicted = get_predict_data(v, date)
        if stock_predicted is not None:
            predicted_list.append(stock_predicted)
            code_list.append(c)

    if 0 == len(predicted_list):
        return None
    
    predict_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": np.array(predicted_list)},
      num_epochs=1,
      shuffle=False)
    
    predictions = list(classifier.predict(input_fn=predict_input_fn))
#     predicted_classes = int(predictions[0]["classes"][0])
#     predicted_probability = predictions[0]['probabilities'][predicted_classes]
    # print("  {} {} {} {}".format(code, date, predicted_classes, predicted_probability))
    
#     return predictions, code_list

    result = [[code_list[idx], int(r["classes"][0]), r['probabilities'][int(r["classes"][0])]] for idx, r in enumerate(predictions)]

#     result = [x for x in result if x[2] > 0.8]
    
    for x in result:
        k = stock_dict[x[0]]
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
    
    while start <= end:
        weekday = start.isoweekday()
        if 6 == weekday or 7 == weekday:
            start += one_day
            continue
            
        day_for_predicted = start.strftime('%Y/%m/%d')
        # print(day_for_predicted)
        predict_stock_day(classifier, stock_dict, day_for_predicted)
        
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
    predict_stock_day(classifier, stock_dict, today_str)


def predict_stock_day(classifier, stock_dict, date_str, code=None):
    if date_str is None:
        print("Please provide the date range.")
        return
    
#     for c, v in stock_dict.items():
#         sld.preliminary_data(v)

    day_for_predicted = date_str
#         print(day_for_predicted)

    df = get_predicted_df(classifier, stock_dict, day_for_predicted)
    if df is None or 0 == len(df):
        return


    class_one = len(df[df['class'] == 1])
    rate = class_one/len(df)
    print("{} {}\t{}".format(day_for_predicted, 'up' if rate > 0.8 else 'fall', rate))
    
    if code is not None:
        df = df[df['code'] == code]

    for idx, row in df.iterrows():
        # if row['probability'] > 0.999 and row['class'] == 1 and row['pc'] > 30 :
        if (row['probability'] > 0.99 or row['pc'] > 20) and row['class'] == 1 :
            print("{} {} {}\t {}".format(row['code'], row['class'], row['probability'], row['pc']))