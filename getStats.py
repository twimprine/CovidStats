import sys, json, requests, time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import datetime as dt
from datetime import timedelta

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# If you have saved a local copy of the file
# set READ_FROM_URL to True
READ_FROM_URL = True
LOCAL_JSON_FILE = 'covid-19-cases.json'

# Today's Date
TODAY = pd.to_datetime("today")

# This is the GitHub URL for the Covid Tracking Project
data_loc = ('https://api.covidtracking.com/v1/states/daily.json')

# Read in the data to a pandas DataFrame.
response = requests.get(data_loc)
data = response.json()
df = pd.DataFrame(data)

df.insert(df.shape[-1],'fmtDate',pd.to_datetime(df.date, format='%Y%m%d'))
#df['fmtDate'] = pd.to_datetime(df.date, format='%Y%m%d')

df = df.iloc[::-1]

louisiana = df.loc[df['state'] == 'LA']
date = louisiana['fmtDate']
deathIncrease = louisiana['deathIncrease']
positiveIncrease = louisiana['positiveIncrease']

fig = plt.figure(figsize=(100,40))

louisiana.insert(louisiana.shape[-1],'SMA_3_deathIncrease', louisiana.loc[:,'deathIncrease'].rolling(window=3).mean())
louisiana.insert(louisiana.shape[-1],'SMA_7_deathIncrease', louisiana.loc[:,'deathIncrease'].rolling(window=7).mean())
louisiana.insert(louisiana.shape[-1],'SMA_28_deathIncrease', louisiana.loc[:,'deathIncrease'].rolling(window=28).mean())
louisiana.insert(louisiana.shape[-1],'SMA_90_deathIncrease', louisiana.loc[:,'deathIncrease'].rolling(window=90).mean())


louisiana.insert(louisiana.shape[-1],'SMA_3_positiveIncrease', louisiana.loc[:,'positiveIncrease'].rolling(window=3).mean())
louisiana.insert(louisiana.shape[-1],'SMA_7_positiveIncrease', louisiana.loc[:,'positiveIncrease'].rolling(window=7).mean())
louisiana.insert(louisiana.shape[-1],'SMA_28_positiveIncrease', louisiana.loc[:,'positiveIncrease'].rolling(window=28).mean())
louisiana.insert(louisiana.shape[-1],'SMA_90_positiveIncrease', louisiana.loc[:,'positiveIncrease'].rolling(window=90).mean())

plt.plot_date(date, louisiana['deathIncrease'], linestyle='solid', color= 'black', label='Louisiana Daily Increase in Covid Deaths')
plt.plot_date(date, louisiana['SMA_3_deathIncrease'], color='red', linestyle='solid', label='3 day rolling average')
plt.plot_date(date, louisiana['SMA_7_deathIncrease'], color='magenta', linestyle='solid', label='7 day rolling average')
plt.plot_date(date, louisiana['SMA_28_deathIncrease'], color='orange', linestyle='solid', label='28 day rolling average')
plt.plot_date(date, louisiana['SMA_90_deathIncrease'], color='navy', linestyle='solid', label='90 day rolling average')
plt.grid(b=True, which='both', axis='both')
plt.legend(loc='upper left')
plt.savefig('CovidGraphDeaths' + time.strftime("%Y%m%d") + '.pdf', dpi=300 )
plt.show()

fig = plt.figure(figsize=(100,40))
plt.plot_date(date, positiveIncrease, linestyle='solid', label='Louisiana Daily Increase in Covid Positive Cases')

plt.plot_date(date, louisiana['positiveIncrease'], color='black', linestyle='solid', label='Louisiana Daily Increase in Covid Positive Cases')
plt.plot_date(date, louisiana['SMA_3_positiveIncrease'], color='red', linestyle='solid', label='3 day rolling average')
plt.plot_date(date, louisiana['SMA_7_positiveIncrease'], color='magenta', linestyle='solid', label='7 day rolling average')
plt.plot_date(date, louisiana['SMA_28_positiveIncrease'], color='orange', linestyle='solid', label='28 day rolling average')
plt.plot_date(date, louisiana['SMA_90_positiveIncrease'], color='navy', linestyle='solid', label='90 day rolling average')
plt.grid(b=True, which='both', axis='both')
plt.legend(loc='upper left')
plt.savefig('CovidGraphPositives' + time.strftime("%Y%m%d") + '.pdf', dpi=300 )
plt.show()


