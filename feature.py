#测试
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def _min(sequence):
	'''
		desc: find min
		param: 
			sequence: list
	'''
	if len(sequence) < 1:
		return None
	else:
		return min(sequence)
def avg(sequence):
	'''
		desc: compute average
		param:
			sequence: list
	'''
	if len(sequence) < 1:
		return None
	else:
		return sum(sequence) / len(sequence)  
def median(sequence):
	'''
		desc: find the median value of the list
		param:
			sequence: list
	'''
	if len(sequence) < 1:
		return None
	else:
		sequence.sort()
		return sequence[len(sequence) // 2]
def m2M(data,x):
	'''
		desc: compute the middle value of the last two months for x
		param:
			data: sorted by time_stamp
			x: datetime
	'''
	pays = []
	loc = list(data['time_stamp']).index(pd.Timestamp(x))
	monthDays = 30
	for i in range(1,monthDays*2):
		print data.loc[loc-i]['time_stamp'],data.loc[loc-i]['pay_sum']
		pays.append(data.loc[loc-i]['pay_sum'])
	return median(pays)
def w2A(data,x):
	'''
		desc: compute average value of the last two weeks
		param:
			data: sorted by time_stamp
			x: datetime
	'''
	pays = []
	loc = list(data['time_stamp']).index(pd.Timestamp(x))
	weekDays = 7
	for i in range(1,weekDays*2):
		print data.loc[loc-i]['time_stamp'],data.loc[loc-i]['pay_sum']
		pays.append(data.loc[loc-i]['pay_sum'])
	return avg(pays)
def m1L(data,x):
	'''
		desc: compute the least valus of the last month
		param: 
			x: datetime
	'''
	pays = []
	loc = list(data['time_stamp']).index(pd.Timestamp(x))
	monthDays = 30
	for i in range(1,monthDays*1):
		print data.loc[loc-i]['time_stamp'],data.loc[loc-i]['pay_sum']
		pays.append(data.loc[loc-i]['pay_sum'])
	return _min(pays)

def d3w3(data,x):
	'''
		desc: compute the average value of the last 3 days and divided by the last 3 weeks
		param:
			x: datetime
	'''
	pays3D = []
	pays3W = []
	loc = list(data['time_stamp']).index(pd.Timestamp(x))
	weekDays = 30
	for i in range(1,weekDays*3):
		print data.loc[loc-i]['time_stamp'],data.loc[loc-i]['pay_sum']
		if i<= 3:
			pays3D.append(data.loc[loc-i]['pay_sum'])
			pays3W.append(data.loc[loc-i]['pay_sum'])
		else:
			pays3W.append(data.loc[loc-i]['pay_sum'])
	return float(avg(pays3D))/avg(pays3W)

if __name__ == '__main__':
	data = pd.read_csv('raw-data/1',index_col='time_stamp')
	sortedData = data.sort_index()
	index = np.array([x for x in range(len(sortedData))])
	sortedData=sortedData.reset_index()
	sortedData['time_stamp'] = pd.to_datetime(sortedData['time_stamp'])
	realStartTime = '2016-09-01'
	
	m2Data = sortedData[sortedData['time_stamp'] >= pd.Timestamp(realStartTime)]
	m2Data['dayofweek'] = map(lambda x:x.dayofweek,m2Data['time_stamp'])
	m2Data['m2M'] = map(lambda x:m2M(sortedData,x),m2Data['time_stamp'])
	m2Data['w2A'] = map(lambda x:w2A(sortedData,x),m2Data['time_stamp'])
	m2Data['m1L'] = map(lambda x:m1L(sortedData,x),m2Data['time_stamp'])
	m2Data['d3w3'] = map(lambda x:d3w3(sortedData,x),m2Data['time_stamp'])
    	f = open('1','w')
	niceData = m2Data.loc[:,['dayofweek','m2M','w2A','m1L','d3w3','pay_sum']]
	niceData.to_csv(f,index=False)
	f.close()
