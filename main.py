import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.neighbors import KDTree
from math import e

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

all_data = pd.concat((train.loc[:,'MSSubClass':'SaleCondition'],test.loc[:,'MSSubClass':'SaleCondition']), ignore_index=True)
price_data = np.log1p(train['SalePrice'])
for col in all_data:
	if all_data[col].dtype==object:
		max_occur = max(all_data[col])
		all_data[col] = all_data[col].fillna(max_occur)
		all_data[col] = all_data[col].astype('category')
	else:
		mean_value = all_data[col].mean()
		all_data[col] = all_data[col].fillna(mean_value)

cat_columns = all_data.select_dtypes(['category']).columns
all_data[cat_columns] = all_data[cat_columns].apply(lambda x: x.cat.codes)
all_data = (all_data - all_data.mean()) / (all_data.max() - all_data.min())
test_data = all_data[0:1460]
print "Id,SalePrice"
for i in range(1460,2919):
	cur_data = test_data
	cur_data = cur_data.append(all_data[i:i+1])
	kdt = KDTree(cur_data, leaf_size=30, metric='euclidean')
	b,a = kdt.query(cur_data[-1:], k=15)
	temp = a[len(a)-1][1:]
	s = 0.0
	for j in range(len(temp)):
		s += price_data[temp[j]]
	s = s/len(temp)
	print "%d,%f" %(i+1,np.expm1(s))