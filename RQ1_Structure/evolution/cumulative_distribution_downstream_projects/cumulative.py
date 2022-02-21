import csv
import datetime
from collections import defaultdict
import statsmodels.api as sm 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


file1 = open('torch_edges.csv', 'r')
csv_reader = csv.reader(file1)
header = next(csv_reader)

created_timestamps = {'pytorch_pytorch': '2017-03-01 00:00:00'}
for row in csv_reader:
	if row[0] not in created_timestamps.keys() or (row[2] is not '' and row[2] < created_timestamps[row[0]]):
		created_timestamps[row[0]] = row[2]
	else:
		continue
file1.close()
print(created_timestamps['pytorch_pytorch'])

file2 = open('torch_edges1.csv', 'w')
csv_writer = csv.writer(file2)
csv_writer.writerow(['lower_nodes','upper_nodes','import_time','layer', 'created_time'])

file1 = open('torch_edges.csv', 'r')
csv_reader = csv.reader(file1)
header = next(csv_reader)
i = 0
for row in csv_reader:
	#print(row)
	if row[1] in created_timestamps.keys():
		csv_writer.writerow(row + [created_timestamps[row[1]]])
	else:
		i += 1
		print(row)
print(i)
file1.close()
file2.close()

file = open('torch_edges1.csv', 'r')
csv_reader = csv.reader(file)
header = next(csv_reader)

d = defaultdict(list)
for row in csv_reader:
	d[(row[1], datetime.datetime.strptime(row[4].split()[0], "%Y-%m-%d"))].append(datetime.datetime.strptime(row[2].split()[0], "%Y-%m-%d"))

for key in d:
	d[key].sort()
print(len(d))
file.close()

#the fraction of time to obtain the 10% of total downstream projects
d_10_percent = []
d_50_percent = []
d_90_percent = []
for i in d:
	n = len(d[i])
	# the number of downstream projects is more than 5
	if n >= 5:
		#print(d[i][int(n*0.1)], d[i][0], d[i][int(n*0.1)] - d[i][0])
		#print((d[i][int(n*0.1)] - d[i][0]).days, (d[i][-1] - d[i][0]).days, d[i])
		fraction_10 = (d[i][int(n*0.1)] - i[1]).total_seconds()/((datetime.datetime.strptime("2020-01-30","%Y-%m-%d") - i[1]).total_seconds()+1)
		if fraction_10 >= 0:
			d_10_percent.append(fraction_10)


		fraction_50 = (d[i][int(n*0.5)] - i[1]).total_seconds()/((datetime.datetime.strptime("2020-01-30","%Y-%m-%d") - i[1]).total_seconds()+1)
		if fraction_50 >= 0:
			d_50_percent.append(fraction_50)


		fraction_90 = (d[i][int(n*0.9)] - i[1]).total_seconds()/((datetime.datetime.strptime("2020-01-30","%Y-%m-%d") - i[1]).total_seconds()+1)
		if fraction_90 >= 0:
			d_90_percent.append(fraction_90)

print(sorted(d_10_percent))

# draw cumulative distribution
fig, ax = plt.subplots()

ecdf_10 = sm.distributions.ECDF(d_10_percent)

x_10 = np.linspace(min(d_10_percent), 1)

y_10 = ecdf_10(x_10)
ax.plot(x_10, y_10, '-', color='k', label = "≥ 10% of total downstream projects")

ecdf_50 = sm.distributions.ECDF(d_50_percent)
x_50 = np.linspace(min(d_50_percent), 1)
y_50 = ecdf_50(x_50)
ax.plot(x_50, y_50, '--', color='b', label = "≥ 50% of total downstream projects")

ecdf_90 = sm.distributions.ECDF(d_90_percent)
x_90 = np.linspace(min(d_90_percent), 1)
y_90 = ecdf_90(x_90)
ax.plot(x_90, y_90, '-.', color='r', label = "≥ 90% of total downstream projects")

plt.rcParams['figure.figsize'] = (5, 6.5)

plt.xlabel('Fraction of time since created − f')
plt.ylabel('Prob. (Fraction of time since created ≤ f)')
#ax.legend(loc='lower right', shadow=True, fontsize='small')
plt.show()
 


# distribution of downstream projects
num_distribution = []
for i in d:
	n = len(d[i])
	num_distribution.append(n)
print(pd.DataFrame(num_distribution).describe())