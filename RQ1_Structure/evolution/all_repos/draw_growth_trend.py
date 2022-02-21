 #-*-coding:utf-8 -*-
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

def prepare_data(f, pos, min_time, max_time):
	time_count = {}
	with open(f) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				line_count += 1
				continue
			start_time = row[pos].split(' ')[0]
			start_times = start_time.split('-')
			start_month = int(start_times[0])*100+int(start_times[1])
			if start_month < min_time:
				continue
			if start_month > max_time:
				continue
			if start_month in time_count.keys():
				time_count[start_month] += 1
			else:
				time_count[start_month] = 1
	
	keys = [min_time]
	start = int(min_time)
	while start < int(max_time):
		year = int(start/100)
		month = int(start - year*100)
		#print(start, year, month)
		if month < 12:
			start += 1
		else:
			start = (year + 1) * 100 + 1
		keys.append(start)
		print(start)
	print(time_count)
	sorted_value = []
	for t in keys:
		if t in time_count.keys():
			sorted_value.append(time_count[t])
		else:
			sorted_value.append(0)

	return sorted_value, [str(k) for k in keys]
		
def draw_line_char(f1, f2, min_time, max_time, ylim1, ylime2, title, fname):
	plt.rcParams['font.sans-serif'] = ['SimHei'] 
	plt.rcParams['axes.unicode_minus'] = False  
	sns.set(font='SimHei', style='white', ) 
	sns.set_style("ticks")
	
	y1, sorted_time_str1 = prepare_data(f1, 1, min_time, max_time)
	y2, sorted_time_str2= prepare_data(f2, 2, min_time, max_time)
	print(y1, sorted_time_str1, y2, sorted_time_str2)
	x = sorted_time_str1

	plt.rcParams['figure.figsize'] = (6.5, 6.5)
	fig = plt.figure()

	ax1 = fig.add_subplot(111)
	ax1.set_ylim([0, ylim1])
	b1 = ax1.bar(x, y1, alpha=0.7, color='k', label= 'project')
	ax1.set_ylabel(u'#project', fontsize='20')
	ax1.set_xlabel(u'time', fontsize='20')
	ax1.tick_params(axis='x',labelsize=16, rotation=45)
	ax1.tick_params(axis='y',labelsize=16)
	ax1.xaxis.set_major_locator(ticker.MultipleLocator(4))



	ax2 = ax1.twinx() 
	ax2.set_ylim([0, ylime2])      
	b2, = ax2.plot(x, y2, color=sns.xkcd_rgb["blue"], ms=8, lw=3, marker='o', label= 'package') 
	ax2.tick_params(labelsize=16, rotation=0)
	sns.despine(left=False, bottom=False, right=False, top=False)   
	plt.legend(handles = [b1,b2], fontsize = 20, loc = 'upper left')
	ax1.set_title(title, fontsize = 20)
	ax2.xaxis.set_major_locator(ticker.MultipleLocator(4))


	plt.savefig("%s.pdf"%(fname), bbox_inches='tight')


fname1 = 'tensorflow_repo_time.csv'
fname2 = 'tensorflow_package_time.csv'
draw_line_char(fname1, fname2, 201511, 201910, 17500, 70, '', "tf")

fname1 = 'torch_repo_time.csv'
fname2 = 'torch_package_time.csv'
draw_line_char(fname1, fname2, 201703, 201910, 10000, 60, '', "torch")

