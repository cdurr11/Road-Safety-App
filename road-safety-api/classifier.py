from sklearn import svm
from sklearn import preprocessing
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pickle

clf = pickle.load(open('random_forest.sav', 'rb'))
street_data = pd.read_csv("street_segments.csv", index_col=0)

def get_scaled_value(value, mean, std):
    return (value - mean)/ std

max_volume = 165200
min_volume = 0
min_lat = 41.644670131999995
max_lat = 42.022779861
min_long = -87.933976504
max_long = -87.52458738699998
avg_temp_mean = 52.736361
avg_temp_std = 20.625818
avg_rain_mean = 0.117716
avg_rain_std = 0.329548
avg_snow_mean = 0.012092
avg_snow_std = 0.104858
length_mean = 439.04927
length_std = 207.835484

street_data[['hour']] = (street_data[['hour']] - 12)/ 12
street_data[['month']] = (street_data[['month']] - 6) / 6

street_data = pd.concat([street_data,pd.get_dummies(street_data['weekday'], prefix='weekday')],axis=1)
street_data = street_data.drop(['weekday'], axis=1)

street_data[['Avg Temp']] = get_scaled_value(street_data[['Avg Temp']], avg_temp_mean, avg_temp_std)
street_data[['Precipitation Water Equiv']] = get_scaled_value(street_data[['Precipitation Water Equiv']], avg_rain_mean, avg_rain_std)
street_data[['Snowfall']] = get_scaled_value(street_data[['Snowfall']], avg_snow_mean, avg_snow_std)
street_data[['length']] = get_scaled_value(street_data[['length']], avg_snow_mean, avg_snow_std)

one_hot_cols = ['weekday_0',
       'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5',
       'weekday_6', 'class_1', 'class_2', 'class_3', 'class_4', 'class_5',
       'class_7', 'class_9', 'class_99', 'class_E', 'class_RIV', 'class_S']

cols = set(street_data.columns.tolist())
for col in one_hot_cols:
    if col not in cols:
        street_data[col] = 0

X = street_data[['hour', 'latitude', 'length', 'longitude', 'month', 'volume',
       'Avg Temp', 'Precipitation Water Equiv', 'Snowfall', 'weekday_0',
       'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5',
       'weekday_6', 'class_1', 'class_2', 'class_3', 'class_4', 'class_5',
       'class_7', 'class_9', 'class_99', 'class_E', 'class_RIV', 'class_S',
       'one_way']]

preds_y = clf.predict_proba(X)
safety_scores = pd.Series(preds_y[:,0].tolist())
street_segs = street_data[['latitude', 'longitude']]
street_segs['safety_score'] = safety_scores.values