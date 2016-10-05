import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.neighbors import KDTree
from sklearn.cluster import KMeans
from math import e
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn import linear_model
from sklearn.cross_validation import cross_val_score

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

o=[30, 462, 523, 632, 968, 970, 1298, 1324]
obj_array = ["MSZoning","Utilities","Exterior1st","Exterior2nd","MasVnrType","Electrical","KitchenQual","Functional","SaleType"]
all_data = pd.concat((train.loc[:,'MSSubClass':'SaleCondition'],test.loc[:,'MSSubClass':'SaleCondition']), ignore_index=True)
price_data = (train['SalePrice'])

all_data=all_data.drop(o,axis=0)
price_data = price_data.drop(o,axis=0)

for col in all_data:
	if all_data[col].dtype==object:
		df1 = all_data[col].value_counts()
		max_occur = df1.index[0]
		all_data[col] = all_data[col].fillna(max_occur)
		all_data[col] = all_data[col].astype('category')
	else:
		mean_value = all_data[col].mean()
		all_data[col] = all_data[col].fillna(mean_value)

cat_columns = all_data.select_dtypes(['category']).columns
all_data[cat_columns] = all_data[cat_columns].apply(lambda x: x.cat.codes)
all_data = (all_data - all_data.mean()) / (all_data.max() - all_data.min())
corr_data = all_data[0:1452]
corr_array = []
for col in corr_data:
	corr_array.append(corr_data[col].corr(price_data))
i=0
for col in all_data:
	all_data[col] = all_data[col]*corr_array[i]
	i+=1

reg = linear_model.Ridge (alpha = .5)
train_data = all_data[0:1452]
test_data = all_data[1452:]
kmeans = KMeans(n_clusters=10, random_state=0).fit(train_data)
temparray = kmeans.predict(train_data)

clf = RandomForestClassifier(random_state=0,n_estimators=50)
print "Id,SalePrice"
for i in range(1452,2911):
	cur_data = train_data
	cur_data = cur_data.append(all_data[i:i+1])
	temparray = kmeans.predict(cur_data)
	value = temparray[-1]
	temparray = temparray[:-1]
	tempotrain = train_data[0:1]
	tempoprice = price_data[0:1]
	for j in range(len(temparray)):
		if value==temparray[j]:
			tempotrain = pd.concat([tempotrain, train_data[j:j+1]])
			tempoprice = pd.concat([tempoprice, price_data[j:j+1]])
	tempotrain = tempotrain[1:]
	tempoprice = tempoprice[1:]
	# clf.fit(tempotrain, tempoprice)
	reg.fit(tempotrain,tempoprice)
	a = reg.predict(all_data[i:i+1])
	print "%d,%f" %(i+9,a[0])
	# print a