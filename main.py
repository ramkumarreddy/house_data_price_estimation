import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.neighbors import KDTree, KNeighborsRegressor
from math import e

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

all_data = pd.concat((train.loc[:,'MSSubClass':'SaleCondition'],test.loc[:,'MSSubClass':'SaleCondition']), ignore_index=True)
price_data = (train['SalePrice'])
for col in all_data:
	if all_data[col].dtype==object:
		# max_occur = max(all_data[col])
		# all_data[col] = all_data[col].fillna(max_occur)
		all_data[col] = all_data[col].astype('category')
	else:
		mean_value = all_data[col].mean()
		all_data[col] = all_data[col].fillna(mean_value)

cat_columns = all_data.select_dtypes(['category']).columns
all_data[cat_columns] = all_data[cat_columns].apply(lambda x: x.cat.codes)
all_data = (all_data - all_data.mean()) / (all_data.max() - all_data.min())
corr_data = all_data[0:1460]
corr_array = []
for col in corr_data:
	corr_array.append(corr_data[col].corr(price_data))
i=0
for col in all_data:
	all_data[col] = all_data[col]*corr_array[i]
	i+=1
train_data = all_data[0:1460]
test_data = all_data[1460:]
print "Id,SalePrice"
neigh = KNeighborsRegressor(n_neighbors=5)
neigh.fit(train_data, price_data) 
a=neigh.predict(test_data)
for i in range(len(a)):
	temp = a[i:i+1]
	print "%d,%f" %(i+1461,(temp))