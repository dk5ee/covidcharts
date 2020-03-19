import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as mysheet
import matplotlib.dates as mdates
import numpy as np
import csv
import datetime
import sys


def plotcountry(name, comment, da, va, de, re):
	# clean up filename
	dates = da
	values = np.array(va)
	deceaseds = np.array(de)
	recovered = np.array(re)
	filename = "".join([c for c in name if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

	with mysheet.xkcd():
		fig = mysheet.figure()
		mysheet.plot(dates, values)
		mysheet.plot(dates, recovered)
		mysheet.plot(dates, deceaseds)
		mysheet.legend(['Confirmed ' + str(values[-1]), 'Recovered ' + str(recovered[-1]), 'Deceased ' + str(deceaseds[-1])], loc=2)
		mysheet.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		mysheet.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
		mysheet.gcf().autofmt_xdate()
		mysheet.title(name + " " + comment + "\n" + str(datetime.datetime.now().date()))
		mysheet.savefig('charts/' + filename + '_small.png', dpi=90)
		mysheet.savefig('charts/' + filename + '_300dpi.png', dpi=300)
		mysheet.close(fig);
	# with open('charts/' + filename + '.csv', mode='w') as csv_file:
	# 	csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	# 	for item in da:
	# 		csv_writer.writerow([item.date(), va.pop(0), re.pop(0), de.pop(0)])
	return


regionsinfected = {}
regionsdeceased = {}
regionsrecovered = {}

deceasedfilename = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
recoveredfilename = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
infectedfilename = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'

deceasedfile = open(deceasedfilename, newline='')
recoveredfile = open(recoveredfilename, newline='')
csvfile = open(infectedfilename, newline='')

deceaseddata = csv.reader(deceasedfile, delimiter=',', quotechar='"')
#drop first row, the header
next(deceaseddata)
recovereddata = csv.reader(recoveredfile, delimiter=',', quotechar='"')
#drop first row, the header
next(recovereddata)

infecteddata = csv.reader(csvfile, delimiter=',', quotechar='"')

header = next(infecteddata)
header = header[4:]

dates = [];



for data in header:
	#header contains datetimes
	datetimeobj = datetime.datetime.strptime(data, '%m/%d/%y')
	dates.append (datetimeobj)
for infected in infecteddata:
	deceased = next(deceaseddata)
	deceased = deceased[4:]
	deceased = list(map(int, deceased))
	recovered = next(recovereddata)
	recovered = recovered[4:]
	recovered = list(map(int, recovered))
	state = infected.pop(0)
	region = infected.pop(0).strip()
	name = region
	lat = infected.pop(0)
	long = infected.pop(0)
	
	infectedvalues = list(map(int, infected))
	# TODO:
	# aggregation of regions does not work all times
	if state:
		name = region + " " + state
		if region in regionsinfected.keys():
			olddata = regionsinfected[region]
			oldddata = regionsdeceased[region]
			oldrdata = regionsrecovered[region]
			newdata = [x + y for x, y in zip(infectedvalues, olddata)]
			newddata = [x + y for x, y in zip(deceased, oldddata)]
			newrdata = [x + y for x, y in zip(recovered, oldrdata)]
			regionsinfected[region] = newdata
			regionsdeceased[region] = newddata
			regionsrecovered[region] = newrdata
		else:
			regionsinfected[region] = infectedvalues
			regionsdeceased[region] = deceased
			regionsrecovered[region] = recovered
	# disable plotting of countries for testing
	#plotcountry (name, "CoVid 19 cases", dates, values, deceaseds, recovered)
for region in regionsinfected.keys():
		
	plotcountry (region, "CoVid 19 cases", dates, regionsinfected[region], regionsdeceased[region], regionsrecovered[region])
