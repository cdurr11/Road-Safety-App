from sklearn import svm
from sklearn import preprocessing
import pandas as pd
from sklearn.linear_model import LogisticRegression


def get_scaled_value(value, mean, std):
    return (value - mean)/ std



min_max_scaler = preprocessing.MinMaxScaler()

data_set = pd.read_csv("./data.csv")

data_set = data_set.sample(frac=1).reset_index(drop=True)

y = data_set[['crash']]

data_set[['hour']] = (data_set[['hour']] - 12)/ 12
data_set[['month']] = (data_set[['month']] - 6) / 6
max_volume = 165200
min_volume = 0
data_set[['volume']] = min_max_scaler.fit_transform(data_set[['volume']])
data_set = pd.concat([data_set,pd.get_dummies(data_set['weekday'], prefix='weekday')],axis=1)

avg_temp_mean = data_set[['Avg Temp']].mean(axis = 0)
avg_temp_std = data_set[['Avg Temp']].std(axis = 0)
data_set[['Avg Temp']] = get_scaled_value(data_set[['Avg Temp']], avg_temp_mean, avg_temp_std)

avg_rain_mean = data_set[['Precipitation Water Equiv']].mean(axis = 0)
avg_rain_std = data_set[['Precipitation Water Equiv']].std(axis = 0)
data_set[['Precipitation Water Equiv']] = get_scaled_value(data_set[['Precipitation Water Equiv']], avg_rain_mean, avg_rain_std)

avg_snow_mean = data_set[['Snowfall']].mean(axis = 0)
avg_snow_std = data_set[['Snowfall']].std(axis = 0)
data_set[['Snowfall']] = get_scaled_value(data_set[['Snowfall']], avg_snow_mean, avg_snow_std)

# print(data_set)




X = data_set[['hour', 'month', 'volume', 'Avg Temp', 'Precipitation Water Equiv', 'Snowfall']]

X = X.to_numpy()
y = y.to_numpy()

train_x = X[:-300000, :]
train_y = y[:-300000, 0].tolist()
test_x = X[-300000:, :]
test_y = y[-300000:, 0].tolist()

clf = LogisticRegression(random_state=0, verbose=1, class_weight='balanced').fit(train_x, train_y)
print('done fitting')
preds = clf.predict_proba(test_x)
print(clf.score(test_x, test_y))
print(preds[0][:50])
print(test_y[:50])

# print(train_x.shape, train_y.shape, test_x.shape, test_y.shape)

# clf = svm.SVC(verbose=True)
# clf.fit(train_x, train_y)
# print("Done Fitting")
