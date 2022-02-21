import csv
import datetime
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import scipy.stats as stats

def process(file_name):
	file1 = open(file_name)
	reader = csv.reader(file1)
	next(reader)

	package = {}
	for row in reader:
		if row[1] not in package.keys():
			package[row[1]] = [datetime.datetime.strptime(row[-1].split()[0], "%Y-%m-%d"), datetime.datetime.strptime(row[-3].strip('\n').split()[0], "%Y-%m-%d"), 0, 0, 0]
		elif datetime.datetime.strptime(row[2].split()[0], "%Y-%m-%d") > package[row[1]][1]:
			package[row[1]][1] = datetime.datetime.strptime(row[2].split()[0], "%Y-%m-%d")
		else:
			continue
	#print(package)
	file1.close()

	# package:{start, end, first_week_num, end_week_num, sum, first_week_end, end_week_start}
	for k in package:
		package[k].append(package[k][0] + datetime.timedelta(days=30))
		package[k].append(package[k][1] - datetime.timedelta(days=30))

	file1 = open(file_name)
	reader = csv.reader(file1)
	next(reader)

	for row in reader:
		package[row[1]][4] += 1
		if datetime.datetime.strptime(row[2].split()[0], "%Y-%m-%d") <= package[row[1]][-2]:
			package[row[1]][2] += 1
		elif datetime.datetime.strptime(row[2].split()[0], "%Y-%m-%d") >= package[row[1]][-1]:
			package[row[1]][3] += 1
		else:
			continue
	#print(package)
	new_package_first = []
	new_package_last = []
	for k in package.keys():
		if package[k][4]>=5 and (package[k][1]-package[k][0]).days > 90:
		   new_package_first.append(package[k][2]/package[k][4]) 
		   new_package_last.append(package[k][3]/package[k][4])
		else:
			continue
	return new_package_first, new_package_last
tf_first_month, tf_last_month = process('tensorflow_edges1.csv')
torch_first_month, torch_last_month = process('torch_edges1.csv')

tf_first_month = pd.Series(np.array(tf_first_month))
tf_last_month = pd.Series(np.array(tf_last_month))
torch_first_month = pd.Series(np.array(torch_first_month))
torch_last_month = pd.Series(np.array(torch_last_month))

#print(tf_first_last_month, torch_first_last_month)

data = {'TF_SC_First': tf_first_month, 
'TF_SC_Last': tf_last_month, 
'PT_SC_First': torch_first_month, 
'PT_SC_Last': torch_last_month}
df = pd.DataFrame(data)
df.to_csv('first_last_month.csv')
"""
df.plot.box()
plt.grid(linestyle="--", alpha=0.3)
plt.show()
"""
res1 = stats.mannwhitneyu(tf_first_month, tf_last_month)
res2 = stats.mannwhitneyu(torch_first_month, torch_last_month)
print(res1)
print(res2)

print(df.describe())