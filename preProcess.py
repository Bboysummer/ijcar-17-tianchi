import pandas as pd

def mergeFile(filePath1,filePath2,shop_id):
	'''
		desc:merge user_view and user_pay for specific user
		param:
			filePath1:path of user_pay
			filePath2:path of user_view
	'''

	# load user data(including user_pay and user_view)
	user_pay = pd.read_csv(filePath1,header=None,names=['shop_id','time_stamp','pay_sum'])
	user_view = pd.read_csv(filePath2,header=None,names=['shop_id','time_stamp','view_sum'])
	
	# choose cols in user data to merge
	pay = user_pay.loc[:,['time_stamp','pay_sum']]
	view = user_view.loc[:,['time_stamp','view_sum']]
	merge = pd.merge(view,pay,how='outer')
	headerShop = ['city_name','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name']
	
	# load shop info
	shop_info = pd.read_csv('shop_info.txt')
	
	# merge cols in shop info
	for header in headerShop:
		merge[header]= list(shop_info[shop_info['shop_id']==shop_id][header].iteritems())[0][1]
	f = open('merge/'+str(shop_id),'w')
	merge.to_csv(f,index=False)
	f.close()


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
	splitDataFiles = {'user_pay_group.txt':'user_pay'}
	#for key in splitDataFiles:
	#	splitFile(key,splitDataFiles[key])
	
	#merge file
	numShop = 2000
	for i in range(1,numShop+1):
		user_view = 'user_view/user_view-'+str(i)
		user_pay= 'user_pay/user_pay-'+str(i)
		mergeFile(user_pay,user_view,i)
