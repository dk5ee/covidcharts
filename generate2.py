import matplotlib as mpl
# allow using mpl without running x server
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import csv
import datetime
import sys


def plotcountry(directory, name, comment, dataset):

	dates,  newinfected,  newdeceased,infected,deceased = dataset; 
	# clean up filename
	filename = "".join([c for c in name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

	with plt.xkcd():
		fig = plt.figure()
		plt.plot(dates, infected)
		plt.plot(dates, newinfected)
		plt.plot(dates, deceased)
		plt.plot(dates, newdeceased)
		plt.legend(['Confirmed ' + str(infected[-1]),
				'New Cases ' + str(newinfected[-1]),
				'Deceased ' + str(deceased[-1]),
				'Daily Deceased ' + str(newdeceased[-1])],loc=2, title="latest reported amount")
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		#plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
		plt.gcf().autofmt_xdate()
		plt.title(name + " " + comment + "\nlatest data from " + str(dates[-1].date()))
		plt.savefig(directory+'/' + filename + '_small.png', dpi=90)
		plt.savefig(directory+'/' + filename + '_300dpi.png', dpi=300)
		plt.close(fig)
	with open(directory+'/' + filename + '.csv', mode='w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for item in dates:
			infectedvalue, infected = infected[0], infected[1:]
			deceasedvalue, deceased = deceased[0], deceased[1:]
			newinfectedvalue, newinfected = newinfected[0], newinfected[1:]
			newdeceasedvalue, newdeceased = newdeceased[0], newdeceased[1:]
			csv_writer.writerow([item.date(),newinfectedvalue,newdeceasedvalue, infectedvalue, deceasedvalue])
	return

def plotdataset(datafilename, directory, comment):
	datafile = open(datafilename, newline='')
	data = csv.reader(datafile, delimiter=',', quotechar='"')
	#skip header 'date,location,new_cases,new_deaths,total_cases,total_deaths'
	next(data)
	
	alllocations = {}
	for item in data:
		date, location, newcases, newdeceased,totalcases, totaldeceased=item
		date = datetime.datetime.strptime(date,('%Y-%m-%d'))
		if newcases == '':
			newcases = '0'
		if newdeceased == '':
			newdeceased = '0'
		if totalcases == '':
			totalcases = '0'
		if totaldeceased == '':
			totaldeceased = '0'
		newcases = int(newcases)
		newdeceased = int(newdeceased)
		totalcases = int(totalcases)
		totaldeceased = int(totaldeceased)
		locationdata = [[],[],[],[],[]]
		if location in alllocations.keys():
			locationdata = alllocations[location]
		locationdata[0].append(date)
		
		locationdata[1].append(newcases)
		locationdata[2].append(newdeceased)
		locationdata[3].append(totalcases)
		locationdata[4].append(totaldeceased)
		alllocations[location] =locationdata
	for key, value in alllocations.items():
		print (key)
		plotcountry (directory, key, comment, value)
	return

plotdataset("coronadata/ecdc/full_data.csv","ecdc", "CoVid19 ECDC")
plotdataset("coronadata/who/full_data.csv","who", "CoVid19 WHO")
