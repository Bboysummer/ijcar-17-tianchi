from feature import *
import numpy as np
import xgboost as xgb
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cross_validation import KFold
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.datasets import load_boston

# set seed
rng = np.random.RandomState(10)

# model weights
weights = [0.20,0.30,0.40,0.10]

# load data(506x13)
#boston = load_boston()
#y = boston['target']
#X = boston['data']
data = pd.read_csv('1')
y = data.loc[:,['pay_sum']].as_matrix()
X = data.loc[:,['dayofweek','m2M','w2A','m1L','d3w3']].as_matrix()

# models set
regressors = []
# xgboost
params_xgb = {}
xgbr=xgb.XGBRegressor(**params_xgb)
regressors.append(xgbr)
# gbr
params_gbm = {}
gbr = GradientBoostingRegressor(**params_gbm)
regressors.append(gbr)
# svr
params_svr = {}
svr = SVR(**params_svr)
regressors.append(svr)
# rfr
params_rfr = {}
rfr = RandomForestRegressor(**params_rfr)
regressors.append(rfr)

# training
for reg in regressors:
	kf = KFold(y.shape[0], n_folds=3, shuffle=True, random_state=rng)
	for train_index, test_index in kf:
    		reg.fit(X[train_index],y[train_index].ravel())

# predict
preStartTime = '2016-11-01'
preEndTime = '2016-11-14'
daysRange = pd.date_range(preStartTime,preEndTime)

# origin data
data1 = pd.read_csv('raw-data/1',index_col='time_stamp')
sortedData = data1.sort_index()
index = np.array([x for x in range(len(sortedData))])
sortedData=sortedData.reset_index()
sortedData['time_stamp'] = pd.to_datetime(sortedData['time_stamp'])

for i in range(0,len(daysRange)):

		# insert pre datetime to sortedData
		insertDay = pd.DataFrame([[daysRange[i],0]],columns=['time_stamp','pay_sum'])
		sortedData = pd.concat([sortedData,insertDay],ignore_index=True)
		loc = list(sortedData['time_stamp']).index(pd.Timestamp(daysRange[i]))
		
		# compute feature vals
		_dayofweek=daysRange[i].dayofweek
		_m2M=m2M(sortedData,daysRange[i])
		_w2A=w2A(sortedData,daysRange[i])
		_m1L=m1L(sortedData,pd.Timestamp(daysRange[i]))
		_d3w3=d3w3(sortedData,pd.Timestamp(daysRange[i]))
		
		# insert feature to data(feature data)
		insertDay_2 = pd.DataFrame([[0,_dayofweek,_m2M,_w2A,_m1L,_d3w3]],columns=['pay_sum','dayofweek','m2M','w2A','m1L','d3w3'])
		data = pd.concat([data,insertDay_2],ignore_index=True)
        	
		# predict vals
		preVals = []
		sampleIndex = len(data)-1
		for reg in regressors:
			sample = []
			newSample = data.loc[sampleIndex]
			sample.append(newSample['dayofweek'])
			sample.append(newSample['m2M'])
			sample.append(newSample['w2A'])
			sample.append(newSample['m1L'])
			sample.append(newSample['d3w3'])
			#sample = np.array([data.loc[sampleIndex].tolist()])
			saple = np.array([sample])
			preVals.append(reg.predict(sample))	
		weights = np.array(weights)
		preVals = np.array(preVals)
		weights.shape = (4,1)
		weights = np.transpose(weights)
		comVals = weights.dot(preVals)
		
		# insert pre vals to sortedData as pay_sum for the next datetime
		sortedData=sortedData.drop(loc)
		insertDay = pd.DataFrame([[comVals[0][0],daysRange[i]]],columns=['pay_sum','time_stamp'])
		
		sortedData = pd.concat([sortedData,insertDay],ignore_index=True)

f1 = open('data','w')
data.to_csv(f1,index=False)
f1.close()
f2 = open('sortedData','w')
sortedData.to_csv(f2,index=False)
f2.close()
# compute error
preVals = []
_X = data.loc[:,['dayofweek','m2M','w2A','m1L','d3w3']].as_matrix()
for reg in regressors:
	preVals.append(reg.predict(_X))
weights = np.array(weights)
preVals = np.array(preVals)
weights.shape = (4,1)
weights = np.transpose(weights)
comVals = weights.dot(preVals)
data['predict']=comVals.tolist()[0]
label = ['pay_sum','predict']
labelColor = ['red','green']
for i in range(0,len(label)):
	plt.plot(data[label[i]],color=labelColor[i],label=label[i])
plt.legend(loc='best')
plt.title('1')
plt.show()
plt.close()
#print "predict vals:",comVals
# total error
#err = (np.absolute(comVals - y.T)/np.absolute(comVals + y.T)).sum()
#print "score:",err

