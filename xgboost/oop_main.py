'''
	desc: main.py
	author: zhpmatrix@datarush
'''
import xgboost as xgb
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.datasets import load_boston
from sklearn.svm import SVR

class Tool:
	def loadData(self,filePath):
		return load_boston()
	def visualize(self):
		return None
class Regressor:
	def setParams(self,params):
		self.params = params
class _SVR(Regressor):
	def __init__(self,params=None):
		self.svr = SVR(params)
	def getSVR(self):
		return self.svr
	def fit(self):
		return None
	def predict(self):
		return None
class Factory:
	def getRegressor(self,name,params):
		if name == "SVR":
			return _SVR(params)
class Model:
	def __init__(self,rSet,X,y,n_folds=3,shuffle=True,random_state=10):
		preSet = []
		self.preSet = preSet
		self.n_folds = n_folds
		self.shuffle = shuffle
		self.random_state = random_state
		self.X = X
		self.y = y
		self.rSet = rSet
		return None

	def train(self):
		kf = KFold(self.y.shape[0],self.n_folds,self.shuffle,self.random_state)
		for regressor in self.rSet:
			for train_index,test_index in kf:
				####################################
				# Bug: None is not in list
				####################################
    				regressor.fit(self.X[train_index],self.y[train_index])
		preSet.append(regressor.predict(self.X))
		return self.preSet

if __name__ == '__main__':

	seed = np.random.RandomState(10)
	filePath = ""
	rSet = []
	preSet = []
	tool = Tool()
	factory = Factory()
	boston = tool.loadData(filePath)
	y = boston['target']
	X = boston['data']
	svr = factory.getRegressor("SVR",None).getSVR()
	rSet.append(svr)
	model = Model(rSet,X,y)
	preSet = model.train()
