 #-*-coding:utf-8 -*-
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

def prepare_data(f, min_time, max_time, layer):
	time_count = {}
	with open(f) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			if int(row[2]) == layer:
				start_time = row[1].split(' ')[0]
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

	keys = []
	keys.append(min_time)
	start = int(min_time)
	while start < int(max_time):
		year = int(start/100)
		month = int(start - year*100)
		if month < 12:
			start += 1
		else:
			start = (year + 1) * 100 + 1
		keys.append(start)
	sorted_value = []
	for t in keys:
		if t in time_count.keys():
			sorted_value.append(time_count[t])
		else:
			sorted_value.append(0)
	for i, t in enumerate(sorted_value):
		if t == 0:
			continue
		else:
			break
	print(layer, sorted_value[i:], [str(k) for k in keys][i:])
	return sorted_value[i:], [str(k) for k in keys][i:]
		
def draw_line_char(f1, min_time, max_time, ylim1, fname):
	plt.rcParams['figure.figsize'] = (12.0, 6.5)
	plt.rcParams['font.sans-serif'] = ['SimHei']  
	plt.rcParams['axes.unicode_minus'] = False  
	sns.set(font='SimHei', style='white', ) 
	sns.set_style("ticks")
	
	y1, sorted_time_str1 = prepare_data(f1, min_time, max_time, 1)
	y2, sorted_time_str2 = prepare_data(f1, min_time, max_time, 2)
	y3, sorted_time_str3 = prepare_data(f1, min_time, max_time, 3)
	y4, sorted_time_str4 = prepare_data(f1, min_time, max_time, 4)
	y5, sorted_time_str5 = prepare_data(f1, min_time, max_time, 5)
	y6, sorted_time_str6 = prepare_data(f1, min_time, max_time, 6)

	fig, ax = plt.subplots(1, 1) 
	ax.plot(sorted_time_str1, y1, color='black', label='layer1', linestyle = '-.')
	ax.plot(sorted_time_str2, y2, color='green', label='layer2', marker = 'o', markersize=3)
	ax.plot(sorted_time_str3, [i*5 for i in y3], color='red', label='layer3*5', linestyle = '-')
	ax.plot(sorted_time_str4, [i*50 for i in y4],  color='skyblue', label='layer4*50', linestyle = '--')
	ax.plot(sorted_time_str5, [i*100 for i in y5], color='blue', label='layer5*100', linestyle = ':')
	
	plt.legend(fontsize = 20, loc = 'upper left') 
	plt.xticks(rotation=45, fontsize=20)
	plt.yticks(fontsize=20)
	plt.xlabel('time', fontsize = 20)
	plt.ylabel('#project', fontsize = 20)
	ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
	
	plt.savefig("%s.pdf"%(fname), bbox_inches='tight')


"""
fname1 = 'tensorflow_info.csv'
draw_line_char(fname1, 201511, 201910, 17500, 'Number of Repos in the different layers of the TensorFlow Supply Chain')

"""
fname1 = 'tensorflow_info.csv'
draw_line_char(fname1, 201511, 201910, 17500, 'tf_different_layer')

