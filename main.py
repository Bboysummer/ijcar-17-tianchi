import numpy as np
import xgboost as xgb
from sklearn.cross_validation import KFold
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.datasets import load_boston

# set seed
rng = np.random.RandomState(10)

# model weights
weights = [0.20,0.30,0.40,0.10]

# predict vals
preVals = []

# combination vals with weights
comVals = []

# load data(506x13)
boston = load_boston()
y = boston['target']
X = boston['data']

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
    		reg.fit(X[train_index],y[train_index])
	preVals.append(reg.predict(X))

weights = np.array(weights)
preVals = np.array(preVals)
weights.shape = (len(weights),1)
weights = np.transpose(weights)

# compute error
comVals = weights.dot(preVals)
# total error
err = (np.absolute(comVals - y.T)/np.absolute(comVals + y.T)).sum()
print err

