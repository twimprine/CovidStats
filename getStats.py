import sys, json, requests, time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import datetime as dt
from datetime import timedelta, datetime
import os

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# If you have saved a local copy of the file
# set READ_FROM_URL to True
READ_FROM_URL = True
LOCAL_JSON_FILE = 'covid-19-cases.json'

# Today's Date
TODAY = pd.to_datetime("today")
currentDir = os.getcwd()

reportDir = os.path.join(currentDir, TODAY.strftime("%Y%m%d"))
os.makedirs(reportDir, exist_ok = True)

print(reportDir)

# This is the GitHub URL for the Covid Tracking Project
data_loc = ('https://api.covidtracking.com/v1/states/daily.json')
states_url = ('https://gist.githubusercontent.com/mshafrir/2646763/raw/8b0dbb93521f5d6889502305335104218454c2bf/states_titlecase.json')

states_response = requests.get(states_url)
states_data = states_response.json()
states_df = pd.DataFrame(states_data)


# Read in the data to a pandas DataFrame.
response = requests.get(data_loc)
data = response.json()
df = pd.DataFrame(data)

#df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')


df.insert(df.shape[-1],'fmtDate',pd.to_datetime(df.date, format='%Y%m%d'))
#df['fmtDate'] = pd.to_datetime(df.date, format='%Y%m%d')
#df = df[df.date != 6]

df = df.iloc[::-1]


for index, row in states_df.iterrows():
    print(row['name'],row['abbreviation'])
    
    state = df.loc[df['state'] == row['abbreviation']]
    
    deathIncrease = state['deathIncrease']
    positiveIncrease = state['positiveIncrease']
    
    fig = plt.figure(figsize=(100,40))

    state.insert(state.shape[-1],'SMA_3_deathIncrease', state.loc[:,'deathIncrease'].rolling(window=3).mean())
    state.insert(state.shape[-1],'SMA_7_deathIncrease', state.loc[:,'deathIncrease'].rolling(window=7).mean())
    state.insert(state.shape[-1],'SMA_28_deathIncrease', state.loc[:,'deathIncrease'].rolling(window=28).mean())
    state.insert(state.shape[-1],'SMA_90_deathIncrease', state.loc[:,'deathIncrease'].rolling(window=90).mean())


    state.insert(state.shape[-1],'SMA_3_positiveIncrease', state.loc[:,'positiveIncrease'].rolling(window=3).mean())
    state.insert(state.shape[-1],'SMA_7_positiveIncrease', state.loc[:,'positiveIncrease'].rolling(window=7).mean())
    state.insert(state.shape[-1],'SMA_28_positiveIncrease', state.loc[:,'positiveIncrease'].rolling(window=28).mean())
    state.insert(state.shape[-1],'SMA_90_positiveIncrease', state.loc[:,'positiveIncrease'].rolling(window=90).mean())

    labelText = row['name'] + "Daily Increase in Covid Deaths - " + time.strftime("%Y%m%d_%H:%M")
    plt.plot_date(state['fmtDate'], state['deathIncrease'], linestyle='solid', color= 'black', label=labelText)
    plt.plot_date(state['fmtDate'], state['SMA_3_deathIncrease'], color='red', linestyle='solid', label='3 day rolling average')
    plt.plot_date(state['fmtDate'], state['SMA_7_deathIncrease'], color='magenta', linestyle='solid', label='7 day rolling average')
    plt.plot_date(state['fmtDate'], state['SMA_28_deathIncrease'], color='orange', linestyle='solid', label='28 day rolling average')
    plt.plot_date(state['fmtDate'], state['SMA_90_deathIncrease'], color='navy', linestyle='solid', label='90 day rolling average')
    plt.grid(b=True, which='both', axis='both')
    plt.legend(loc='upper left')
    fileName = row['name'].replace(" ","_") + '_CovidGraphDeaths' + time.strftime("%Y%m%d") + '.pdf'
    savePath = os.path.join(reportDir, fileName)
    plt.savefig(savePath, dpi=75 )
    #plt.show()
    plt.close()

    fig = plt.figure(figsize=(100,40))
    labelText = row['name'] + "Daily Increase in Covid Positive Cases - " + time.strftime("%Y%m%d_%H:%M")
    plt.plot_date(state['fmtDate'], positiveIncrease, linestyle='solid', label=labelText)

    plt.plot_date(state['fmtDate'], state['positiveIncrease'], color='black', linestyle='solid', label='state Daily Increase in Covid Positive Cases')
    plt.plot_date(state['fmtDate'], state['SMA_3_positiveIncrease'], color='red', linestyle='solid', label='3 day rolling average')
    plt.plot_date(state['fmtDate'], state['SMA_7_positiveIncrease'], color='magenta', linestyle='solid', label='7 day rolling average')
    plt.plot_date(state['fmtDate'], state['SMA_28_positiveIncrease'], color='orange', linestyle='solid', label='28 day rolling average')
    plt.plot_date(state['fmtDate'], state['SMA_90_positiveIncrease'], color='navy', linestyle='solid', label='90 day rolling average')
    plt.grid(b=True, which='both', axis='both')
    plt.legend(loc='upper left')
    fileName = row['name'].replace(" ","_") + '_CovidGraphPositives' + time.strftime("%Y%m%d") + '.pdf'
    savePath = os.path.join(reportDir, fileName)
    plt.savefig(savePath, dpi=75 )
    #plt.show()
    plt.close()

