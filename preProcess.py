import pandas as pd

def splitFile(filePath,fileName,shopNum=2000):
	groupData = pd.read_csv(filePath,header=None,names=['shop_id','time_stamp','sum'])
	for i in range(1,shopNum+1):
		f = open(fileName+'-'+str(i),'w')
		groupData[groupData['shop_id'] == i].to_csv(f,index=False,header=False)
		f.close()
		
def groupFile(filePath,fileName):
	'''
		desc: group the data including user_view and user_pay
		param: 
			filePath: path of file(stupid!)
			fileName: save new file at current directory
	'''
	userData = pd.read_csv(filePath);
	userData['time_stamp'] = map(lambda x: x.strftime('%Y-%m-%d'), pd.to_datetime(userData['time_stamp']))
	groupData = userData.groupby(['shop_id','time_stamp']).size()
	f = open(fileName,'w');
	groupData.to_csv(f);
	f.close();

if __name__ == "__main__":
	dataFiles = {'user_view.txt':'user_view_group.txt',
			'user_pay.txt':'user_pay_group.txt'}
	#for key in dataFiles:
	#	groupFile(key,dataFiles[key])
	splitDataFiles = {'user_view_group.txt':'user_view'}
	for key in splitDataFiles:
		splitFile(key,splitDataFiles[key])
