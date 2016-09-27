import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.neighbors import KDTree, KNeighborsRegressor
from math import e

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

all_data = pd.concat((train.loc[:,'MSSubClass':'SaleCondition'],test.loc[:,'MSSubClass':'SaleCondition']), ignore_index=True)
price_data = np.log1p(train['SalePrice'])
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
train_data = all_data[0:1460]
test_data = all_data[1460:]
print "Id,SalePrice"
neigh = KNeighborsRegressor(n_neighbors=14)
neigh.fit(train_data, price_data) 
a=neigh.predict(test_data)
for i in range(len(a)):
	temp = a[i:i+1]
	print "%d,%f" %(i+1461,np.expm1(temp))