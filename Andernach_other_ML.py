import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import sklearn as sklearn

# load data and arrange into Pandas dataframe
cols=["Evaporation","Precipitation","Temperature","Discharge"]
df=pd.read_excel("C:/Users/thtuh/Desktop/project/Final Data/CDC/for python/sheet 1.xlsx",usecols=cols)

excel_file = 'C:/Users/thtuh/Desktop/project/Final Data/CDC/for python/sheet 1.xlsx'
Dt = pd.read_excel(excel_file,usecols=['Date'])

#Split into parameters and target (Discharge)
#X = df.drop('Discharge', axis = 1)
#y = df['Discharge']


train = df[0:1460]
test  = df[1096:2191]

trainX = train.drop('Discharge', axis = 1)
trainY = train['Discharge']
testX  = test.drop('Discharge', axis = 1)
testY  = test['Discharge']




#trainX, testX, trainY, testY = train_test_split(X, y, test_size = 0.33, random_state = 20)


#Scale data, otherwise model will fail.
#Standardize features by removing the mean and scaling to unit variance

from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
scaler.fit(trainX)

X_train_scaled = scaler.transform(trainX)
X_test_scaled = scaler.transform(testX)


# define the model
#Experiment with deeper and wider networks
model = Sequential()
model.add(Dense(128, input_dim=3, activation='relu'))
model.add(Dense(64, activation='relu'))
#Output layer
model.add(Dense(1, activation='linear'))

model.compile(loss='mse', optimizer='adam', metrics=['mae'])
model.summary()


history = model.fit(X_train_scaled, trainY, validation_split=0.33, epochs =100)


predictions_train =model.predict(X_train_scaled)
predictions_test = model.predict(X_test_scaled)
print("Predicted values are: ", predictions_test[:5])
print("Real values are: ", testY[:5])

plt.plot(testY)
plt.plot(predictions_test)


mse_neural, mae_neural = model.evaluate(X_train_scaled,trainY)
print('Mean squared error from neural net for train: ', mse_neural)
print('Mean absolute error from neural net for train: ', mae_neural)

mse_neural, mae_neural = model.evaluate(X_test_scaled,testY)
print('Mean squared error from neural net for test: ', mse_neural)
print('Mean absolute error from neural net for test: ', mae_neural)


testScore = math.sqrt(mean_squared_error(predictions_test,testY))
print('Test Score: %.2f RMSE' % (testScore))
trainScore = math.sqrt(mean_squared_error(predictions_train,trainY))
print('Train Score: %.2f RMSE' % (trainScore))

print('R^2 Value from train: ', sklearn.metrics.r2_score(predictions_train,trainY))
print('R^2 Value from test: ', sklearn.metrics.r2_score(predictions_test,testY))

from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

### Linear regression
lr_model = linear_model.LinearRegression()
lr_model.fit(trainX,trainY)
y_pred_lr = lr_model.predict(testX)
mse_lr = mean_squared_error(testY, y_pred_lr)
mae_lr = mean_absolute_error(testY, y_pred_lr)
RMSE_lr = math.sqrt(mean_squared_error(testY, y_pred_lr))

print('test Score: %.2f RMSE' % (RMSE_lr))

print('Mean squared error from linear regression for test: ', mse_lr)
print('Mean absolute error from linear regression for test: ', mae_lr)

print('R^2 Value from test: ', sklearn.metrics.r2_score(testY, y_pred_lr))

lr_model.fit(trainX,trainY)
yt_pred_lr = lr_model.predict(trainX)
mse_lrt = mean_squared_error(trainY, yt_pred_lr)
mae_lrt = mean_absolute_error(trainY, yt_pred_lr)
RMSE_lrt = math.sqrt(mean_squared_error(trainY, yt_pred_lr))

print('train Score: %.2f RMSE' % (RMSE_lrt))
print('Mean squared error from linear regression for train: ', mse_lrt)
print('Mean absolute error from linear regression for train: ', mae_lrt)
print('R^2 Value from train: ', sklearn.metrics.r2_score(trainY, yt_pred_lr))



### Decision tree
tree = DecisionTreeRegressor()
tree.fit(trainX, trainY)
y_pred_tree = tree.predict(testX)
mse_dt = mean_squared_error(testY, y_pred_tree)
mae_dt = mean_absolute_error(testY, y_pred_tree)
RMSE_dt = math.sqrt(mean_squared_error(testY, y_pred_tree))

print('R^2 Value from test using decision tree: ', sklearn.metrics.r2_score(testY,y_pred_tree ))
print('test Score: %.2f RMSEusing decisin tree' % (RMSE_dt))
print('Mean squared error using decision tree: ', mse_dt)
print('Mean absolute error using decision tree: ', mae_dt)


yt_pred_tree = tree.predict(trainX)
mse_dtt = mean_squared_error(trainY, yt_pred_tree)
mae_dtt = mean_absolute_error(trainY,yt_pred_tree)
RMSE_dtt = math.sqrt(mean_squared_error(trainY, yt_pred_tree))

print('train Score: %.2f RMSE' % (RMSE_dtt))
print('Mean squared error from decision tree for train: ', mse_dtt)
print('Mean absolute error from decision tree for train: ', mae_dtt)
print('R^2 Value from train using decision tree: ', sklearn.metrics.r2_score(trainY,  yt_pred_tree))
##############################################
#Random forest.
#Increase number of tress and see the effect
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators = 30, random_state=30)
model.fit(trainX, trainY)

y_pred_RF = model.predict(testX)

mse_RF = mean_squared_error(testY, y_pred_RF)
mae_RF = mean_absolute_error(testY, y_pred_RF)
RMSE_RF = math.sqrt(mean_squared_error(testY, y_pred_RF))

print('R^2 Value from test using random forest: ', sklearn.metrics.r2_score(testY,y_pred_RF))
print('test Score: %.2f RMSE' % (RMSE_RF))
print('Mean squared error using Random Forest: ', mse_RF)
print('Mean absolute error Using Random Forest: ', mae_RF)

yt_pred_RF = model.predict(trainX)
mse_RFt = mean_squared_error(trainY, yt_pred_RF)
mae_RFt = mean_absolute_error(trainY,yt_pred_RF)
RMSE_RFt = math.sqrt(mean_squared_error(trainY, yt_pred_RF))

print('train Score: %.2f RMSE' % (RMSE_RFt))
print('Mean squared error from random forest for train: ', mse_RFt)
print('Mean absolute error from random forest for train: ', mae_RFt)
print('R^2 Value from train for random forest: ', sklearn.metrics.r2_score(trainY,  yt_pred_RF))







#Feature ranking...
import pandas as pd
feature_list = list(X.columns)
feature_imp = pd.Series(model.feature_importances_, index=feature_list).sort_values(ascending=False)
print(feature_imp)