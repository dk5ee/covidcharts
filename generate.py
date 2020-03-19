import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as mysheet
import matplotlib.dates as mdates
import numpy as np
import csv
import datetime
import sys

def plotcountry( name, comment, da, va, de, re ):
	#clean up filename
	dates=da
	if len(va) ==0:
		return
	if len(da) ==0:
		return
	if len(de) ==0:
		return
	if len(re) ==0:
		return
	values=np.array(va)
	deaths=np.array(de)
	recovered=np.array(re)
	filename = "".join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).rstrip()
#	print(filename)
	with mysheet.xkcd():
		fig = mysheet.figure()
		mysheet.plot(dates,values)
		mysheet.plot(dates,recovered)
		mysheet.plot(dates,deaths)
		mysheet.legend(['Confirmed '+str(values[-1]),'Recovered '+str(recovered[-1]), 'Deceased '+str(deaths[-1])], loc=2)
		mysheet.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		mysheet.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
		mysheet.gcf().autofmt_xdate()
		mysheet.title(name + " " + comment + "\n" + str(datetime.datetime.now().date()))
		mysheet.savefig('charts/' + filename + '_small.png', dpi=90)
		mysheet.savefig('charts/' + filename + '_300dpi.png', dpi=300)
		mysheet.close(fig);
	with open('charts/' + filename+'.csv', mode='w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for item in da:
			csv_writer.writerow([item.date(), va.pop(0),re.pop(0),de.pop(0)])
	return

regionsinfected = {}
regionsdeath = {}
regionsrecovered = {}

deathfile = open('COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
recoveredfile = open('COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')

with open('COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv', newline='') as csvfile:
	deathdata = csv.reader(deathfile, delimiter=',', quotechar='"')
	next(deathdata)
	recovereddata =  csv.reader(recoveredfile, delimiter=',', quotechar='"')
	next(recovereddata)
	mydata = csv.reader(csvfile, delimiter=',', quotechar='"')
	header = next(mydata)
	header = header[4:]
	dates = [];
	for data in header:
		datetimeobj = datetime.datetime.strptime(data, '%m/%d/%y')
		dates.append (datetimeobj)
	for row in mydata:
		deaths=next(deathdata)
		deaths=deaths[4:]
		deaths = list(map(int,deaths))
		recovered=next(recovereddata)
		recovered=recovered[4:]
		recovered = list(map(int,recovered))
		state = row.pop(0)
		region = row.pop(0).strip()
		name = region
		lat = row.pop(0)
		long = row.pop(0)
		values = list(map(int,row))
		# TODO:
		# aggregation of regions does not work all times
		if state:
			name = region+ " " +state
			if region in regionsinfected.keys():
				olddata=regionsinfected[region]
				oldddata = regionsdeath[region]
				oldrdata = regionsrecovered[region]
				newdata = [x + y for x, y in zip(values, olddata)]
				newddata = [x + y for x, y in zip(deaths, oldddata)]
				newrdata = [x + y for x, y in zip(recovered, oldrdata)]
				regionsinfected[region] = newdata
				regionsdeath[region] = newddata
				regionsrecovered[region] = newrdata
			else:
				regionsinfected[region] = values
				regionsdeath[region] = deaths
				regionsrecovered[region] = recovered
		plotcountry (name, "CoVid 19 cases", dates, values,deaths,recovered)
	for region in regionsinfected.keys():
		plotcountry (region, "CoVid 19 cases", dates, regionsinfected[region], regionsdeath[region], regionsrecovered[region])

