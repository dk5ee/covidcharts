import matplotlib as mpl
# allow using mpl without running x server
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import csv
import datetime
import sys


def calculatedeltas(inputarray):
	deltas = [];
	for key in range(len(inputarray)):
		if key == 0:
			deltas.append(inputarray[key])
		else:
			deltas.append(inputarray[key] - inputarray[key - 1])
	return deltas


def plotcountry(name, comment, dates, infected, deceased):
	# clean up filename
	filename = "".join([c for c in name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

	with plt.xkcd():
		fig = plt.figure()
		plt.plot(dates, infected)
		newinfected = calculatedeltas(infected)
		plt.plot(dates, newinfected)
		plt.plot(dates, deceased)
		newdeceased = calculatedeltas(deceased)
		plt.plot(dates, newdeceased)
		plt.legend(['Confirmed ' + str(infected[-1]), 'Daily new cases ' + str(newinfected[-1]), 'Deceased ' + str(deceased[-1]), 'New deceased ' + str(newdeceased[-1])], loc=2)
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
		plt.gcf().autofmt_xdate()
		plt.title(name + " " + comment + "\nlatest data from " + str(dates[-1].date()))
		plt.savefig('charts/' + filename + '_small.png', dpi=90)
		plt.savefig('charts/' + filename + '_300dpi.png', dpi=300)
		plt.close(fig)
	with open('charts/' + filename + '.csv', mode='w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for item in dates:
			infectedvalue, infected = infected[0], infected[1:]
			newinfectedvalue, newinfected = newinfected[0], newinfected[1:]
			deceasedvalue, deceased = deceased[0], deceased[1:]
			newdeceasedvalue, newdeceased = newdeceased[0], newdeceased[1:]
			csv_writer.writerow([item.date(), infectedvalue, newinfectedvalue, deceasedvalue, newdeceasedvalue])
	return


regionsinfected = {}
regionsdeceased = {}

deceasedfilename = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
infectedfilename = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

deceasedfile = open(deceasedfilename, newline='')
infectedfile = open(infectedfilename, newline='')

deceaseddata = csv.reader(deceasedfile, delimiter=',', quotechar='"')
# drop first row, the header
next(deceaseddata)

infecteddata = csv.reader(infectedfile, delimiter=',', quotechar='"')

header = next(infecteddata)
header = header[4:]
dates = []

for data in header:
	# header contains datetimes
	datetimeobj = datetime.datetime.strptime(data, '%m/%d/%y')
	dates.append (datetimeobj)
for infected in infecteddata:
	deceased = next(deceaseddata)
	deceased = deceased[4:]
	deceasedvalues = np.array(list(map(int, deceased)))
	state = infected.pop(0).strip()
	region = infected.pop(0).strip()
	name = region
	lat = infected.pop(0).strip()
	long = infected.pop(0).strip()
	
	infectedvalues = np.array(list(map(int, infected)))
	# print(name + " " + str(infectedvalues.shape) + " " + str(deceasedvalues.shape) + " " + str(recoveredvalues.shape))
	if state:
		# if string for "state" is set, the values of the region are split and need to be aggregated
		name = region + " " + state
		if region in regionsinfected.keys():
			olddata = regionsinfected[region]
			oldddata = regionsdeceased[region]
			newdata = np.add(infectedvalues, olddata)
			newddata = np.add(deceasedvalues, oldddata)
			regionsinfected[region] = newdata
			regionsdeceased[region] = newddata
		else:
			regionsinfected[region] = infectedvalues
			regionsdeceased[region] = deceasedvalues
	plotcountry (name, "CoVid 19 cases", dates, infectedvalues, deceasedvalues)
for region in regionsinfected.keys():
	infectedvalues = regionsinfected[region]
	deceasedvalues = regionsdeceased[region]
	# print(name + " " + str(infectedvalues.shape) + " " + str(deceasedvalues.shape) + " " + str(recoveredvalues.shape))
	plotcountry (region, "CoVid 19 cases", dates, infectedvalues, deceasedvalues)
