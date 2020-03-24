import matplotlib as mpl
# allow using mpl without running x server
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import csv
import datetime
import sys


def plotcountry(name, comment, dates, infected, deceased, recovered):
	# clean up filename
	filename = "".join([c for c in name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

	with plt.xkcd():
		fig = plt.figure()
		plt.plot(dates, infected)
		plt.plot(dates, recovered)
		plt.plot(dates, deceased)
		plt.legend(['Confirmed ' + str(infected[-1]), 'Recovered ' + str(recovered[-1]), 'Deceased ' + str(deceased[-1])], loc=2)
		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
		plt.gcf().autofmt_xdate()
		plt.title(name + " " + comment + "\nlatest data from " + str(dates[-1].date()))
		plt.savefig('oldjhu/' + filename + '_small.png', dpi=90)
		plt.savefig('oldjhu/' + filename + '_300dpi.png', dpi=300)
		plt.close(fig)
	with open('oldjhu/' + filename + '.csv', mode='w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for item in dates:
			infectedvalue, infected = infected[0], infected[1:]
			deceasedvalue, deceased = deceased[0], deceased[1:]
			recoveredvalue, recovered = recovered[0], recovered[1:]
			csv_writer.writerow([item.date(), infectedvalue, recoveredvalue, deceasedvalue])
	return


regionsinfected = {}
regionsdeceased = {}
regionsrecovered = {}

deceasedfilename = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
recoveredfilename = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
infectedfilename = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'

deceasedfile = open(deceasedfilename, newline='')
recoveredfile = open(recoveredfilename, newline='')
infectedfile = open(infectedfilename, newline='')

deceaseddata = csv.reader(deceasedfile, delimiter=',', quotechar='"')
# drop first row, the header
next(deceaseddata)
recovereddata = csv.reader(recoveredfile, delimiter=',', quotechar='"')
# drop first row, the header
next(recovereddata)

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
	recovered = next(recovereddata)
	recovered = recovered[4:]
	recoveredvalues = np.array(list(map(int, recovered)))
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
			oldrdata = regionsrecovered[region]
			newdata = np.add(infectedvalues, olddata)
			newddata = np.add(deceasedvalues, oldddata)
			newrdata = np.add(recoveredvalues, oldrdata)
			regionsinfected[region] = newdata
			regionsdeceased[region] = newddata
			regionsrecovered[region] = newrdata
		else:
			regionsinfected[region] = infectedvalues
			regionsdeceased[region] = deceasedvalues
			regionsrecovered[region] = recoveredvalues
	plotcountry (name, "CoVid 19 cases", dates, infectedvalues, deceasedvalues, recoveredvalues)
for region in regionsinfected.keys():
	infectedvalues = regionsinfected[region]
	deceasedvalues = regionsdeceased[region]
	recoveredvalues = regionsrecovered[region]
	# print(name + " " + str(infectedvalues.shape) + " " + str(deceasedvalues.shape) + " " + str(recoveredvalues.shape))
	plotcountry (region, "CoVid 19 cases", dates, infectedvalues, deceasedvalues, recoveredvalues)
