#!/usr/bin/python3

import sys, json, requests, time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import datetime as dt
from datetime import timedelta, datetime
import os
import numpy as np


# Today's Date
TODAY = pd.to_datetime("today")
currentDir = os.getcwd()

reportDir = os.path.join(currentDir,"reports",  TODAY.strftime("%Y%m%d"))
os.makedirs(reportDir, exist_ok = True)


covid_data_loc = ('https://api.covidtracking.com/v1/states/daily.json')

covid_data_response = requests.get(covid_data_loc)
covid_data = covid_data_response.json()
covid_df = pd.DataFrame(covid_data)

states_url = ('https://raw.githubusercontent.com/twimprine/Datasets/main/states.json')
states_response = requests.get(states_url)
states_data = states_response.json()
states_df = pd.DataFrame(states_data)


covid_df = covid_df.drop(['positive', 'probableCases', 'negative', 'pending',
       'totalTestResultsSource', 'totalTestResults', 'hospitalizedCurrently',
       'hospitalizedCumulative', 'inIcuCumulative',
       'onVentilatorCumulative', 'recovered',
       'dataQualityGrade', 'lastUpdateEt', 'dateModified', 'checkTimeEt',
       'death', 'hospitalized', 'dateChecked', 'totalTestsViral',
       'positiveTestsViral', 'negativeTestsViral', 'positiveCasesViral',
       'deathConfirmed', 'deathProbable', 'totalTestEncountersViral',
       'totalTestsPeopleViral', 'totalTestsAntibody', 'positiveTestsAntibody',
       'negativeTestsAntibody', 'totalTestsPeopleAntibody',
       'positiveTestsPeopleAntibody', 'negativeTestsPeopleAntibody',
       'totalTestsPeopleAntigen', 'positiveTestsPeopleAntigen',
       'totalTestsAntigen', 'positiveTestsAntigen', 'fips', 
       'negativeIncrease', 'total', 'totalTestResultsIncrease', 'posNeg',
        'hash', 'commercialScore',
       'negativeRegularScore', 'negativeScore', 'positiveScore', 'score',
       'grade'],1)

covid_df.insert(covid_df.shape[-1],'fmtDate',pd.to_datetime(covid_df.date, format='%Y%m%d'))
#covid_df.columns

covid_df.set_index(['state','fmtDate'])
covid_df.sort_values(by=['state', 'fmtDate'])
covid_df = covid_df.iloc[::-1]

report_d = {}
report_df = pd.DataFrame(data=report_d)
report_df

for index, row in states_df.iterrows():
    #print(index)
    #print(row)
    state = covid_df.loc[covid_df['state'] == row['abbreviation']]
    loop_df = pd.DataFrame(data=state)
    
    #print('Loop DF:\n', loop_df)
    
    deathIncrease = loop_df['deathIncrease']
    positiveIncrease = loop_df['positiveIncrease']
    population = row['population']['estimates']['2019']
    
    divisor = 0
    
    if population >= 1000000:
        divisor = 100000
    elif population <= 999999 and population > 100000:
        divisor = 10000
    elif population <= 99999 and population > 1000:
        divisor = 1000
    else:
        divisor = 0
    
    
    #print(row['name'],row['abbreviation'],row['population']['estimates']['2019'], divisor)
    if divisor > 0:        
        
        loop_df.insert(loop_df.shape[-1], 'positiveIncreasePopulation', loop_df.loc[:,'positiveIncrease'] / divisor)
        loop_df.insert(loop_df.shape[-1], 'SMA_7_CasesPerPopulation', loop_df.loc[:,'positiveIncrease'].rolling(window=7).mean() / divisor)
        loop_df.insert(loop_df.shape[-1], 'SMA_28_CasesPerPopulation', loop_df.loc[:,'positiveIncrease'].rolling(window=28).mean() / divisor)
        
        loop_df.insert(loop_df.shape[-1], 'deathIncreasePopulation', loop_df.loc[:,'deathIncrease'] / divisor)
        loop_df.insert(loop_df.shape[-1], 'SMA_7_DeathsPerPopulation', loop_df.loc[:,'deathIncrease'].rolling(window=7).mean() / divisor)
        loop_df.insert(loop_df.shape[-1], 'SMA_28_DeathsPerPopulation', loop_df.loc[:,'deathIncrease'].rolling(window=28).mean() / divisor)
        
        
        fig = plt.figure(figsize=(100,40))
        labelText_cases = row['name'] + " Cases per " + str(divisor) + " people"
        plt.plot_date(loop_df['fmtDate'], (loop_df['positiveIncreasePopulation']), color='blue', linestyle='solid', label=labelText_cases)
        plt.plot_date(loop_df['fmtDate'], (loop_df['SMA_7_CasesPerPopulation']), color='deepskyblue', linestyle='solid', label='7 day rolling average')
        plt.plot_date(loop_df['fmtDate'], (loop_df['SMA_28_CasesPerPopulation']), color='fuchsia', linestyle='solid', label='28 day rolling average')
        
        plt.grid(b=True, which='both', axis='both')
        plt.legend(loc='upper left')
        plt.tick_params(labelleft=True, labelright=True, labeltop=True, labelbottom=True)
        fileName = row['name'].replace(" ","_") + '_CovidCasesPopulationStats' + time.strftime("%Y%m%d") + '.pdf'
        savePath = os.path.join(reportDir, fileName)
        plt.savefig(savePath, dpi=75 )
        #plt.show()
        plt.close()
        
        fig = plt.figure(figsize=(100,40))
        labelText_deaths = row['name'] + " Deaths per " + str(divisor) + " people"
        plt.plot_date(loop_df['fmtDate'], (loop_df['deathIncreasePopulation']), color='red', linestyle='solid', label=labelText_deaths)
        plt.plot_date(loop_df['fmtDate'], (loop_df['SMA_7_DeathsPerPopulation']), color='orange', linestyle='solid', label='7 day rolling average')
        plt.plot_date(loop_df['fmtDate'], (loop_df['SMA_28_DeathsPerPopulation']), color='brown', linestyle='solid', label='28 day rolling average')
        
        plt.grid(b=True, which='both', axis='both')
        plt.legend(loc='upper left')
        fileName = row['name'].replace(" ","_") + '_CovidDeathPopulationStats' + time.strftime("%Y%m%d") + '.pdf'
        savePath = os.path.join(reportDir, fileName)
        plt.savefig(savePath, dpi=75 )
        #plt.show()
        plt.close()
        
        
    loop_df.insert(loop_df.shape[-1],'SMA_3_positiveIncrease', loop_df.loc[:,'positiveIncrease'].rolling(window=3).mean())
    loop_df.insert(loop_df.shape[-1],'SMA_7_positiveIncrease', loop_df.loc[:,'positiveIncrease'].rolling(window=7).mean())
    loop_df.insert(loop_df.shape[-1],'SMA_28_positiveIncrease', loop_df.loc[:,'positiveIncrease'].rolling(window=28).mean())
    loop_df.insert(loop_df.shape[-1],'SMA_90_positiveIncrease', loop_df.loc[:,'positiveIncrease'].rolling(window=90).mean())
    
    loop_df.insert(loop_df.shape[-1],'SMA_3_deathIncrease', loop_df.loc[:,'deathIncrease'].rolling(window=3).mean())
    loop_df.insert(loop_df.shape[-1],'SMA_7_deathIncrease', loop_df.loc[:,'deathIncrease'].rolling(window=7).mean())
    loop_df.insert(loop_df.shape[-1],'SMA_28_deathIncrease', loop_df.loc[:,'deathIncrease'].rolling(window=28).mean())
    loop_df.insert(loop_df.shape[-1],'SMA_90_deathIncrease', loop_df.loc[:,'deathIncrease'].rolling(window=90).mean())
    
    
    fig = plt.figure(figsize=(100,40))
    labelText = row['name'] + " Daily Increase in Covid Positive Cases - " + time.strftime("%Y%m%d_%H:%M")
    plt.plot_date(loop_df['fmtDate'], loop_df['positiveIncrease'], color='black', linestyle='solid', label=labelText)
    plt.plot_date(loop_df['fmtDate'], loop_df['SMA_3_positiveIncrease'], color='red', linestyle='solid', label='3 day rolling average')
    plt.plot_date(loop_df['fmtDate'], loop_df['SMA_7_positiveIncrease'], color='magenta', linestyle='solid', label='7 day rolling average')
    plt.plot_date(loop_df['fmtDate'], loop_df['SMA_28_positiveIncrease'], color='orange', linestyle='solid', label='28 day rolling average')
    plt.plot_date(loop_df['fmtDate'], loop_df['SMA_90_positiveIncrease'], color='navy', linestyle='solid', label='90 day rolling average')
    plt.grid(b=True, which='both', axis='both')
    plt.legend(loc='upper left')
    fileName = row['name'].replace(" ","_") + '_CovidGraphPositives' + time.strftime("%Y%m%d") + '.pdf'
    savePath = os.path.join(reportDir, fileName)
    plt.savefig(savePath, dpi=75 )
    #plt.show()
    plt.close()
    
    fig = plt.figure(figsize=(100,40))
    labelText = row['name'] + " Daily Increase in Covid Deaths - " + time.strftime("%Y%m%d_%H:%M")
    plt.plot_date(loop_df['fmtDate'], loop_df['deathIncrease'], linestyle='solid', color= 'black', label=labelText)
    plt.plot_date(loop_df['fmtDate'], loop_df['SMA_3_deathIncrease'], color='red', linestyle='solid', label='3 day rolling average')
    plt.plot_date(loop_df['fmtDate'], loop_df['SMA_7_deathIncrease'], color='magenta', linestyle='solid', label='7 day rolling average')
    plt.plot_date(loop_df['fmtDate'], loop_df['SMA_28_deathIncrease'], color='orange', linestyle='solid', label='28 day rolling average')
    plt.plot_date(loop_df['fmtDate'], loop_df['SMA_90_deathIncrease'], color='navy', linestyle='solid', label='90 day rolling average')
    plt.grid(b=True, which='both', axis='both')
    plt.legend(loc='upper left')
    fileName = row['name'].replace(" ","_") + '_CovidGraphDeaths' + time.strftime("%Y%m%d") + '.pdf'
    savePath = os.path.join(reportDir, fileName)
    plt.savefig(savePath, dpi=75 )
    #plt.show()
    plt.close()
    
    report_df = report_df.append(loop_df, ignore_index=True, sort=False)
    loop_df = pd.DataFrame(data={})

fig = plt.figure(figsize=(100,40))
labelText = "Top 5 States Rate of Transmission - " + time.strftime("%Y%m%d_%H:%M")
colors = ['red','darkorange','darkslategray','purple','darkgreen']
counter = 0

for index, row in report_df.sort_values(by=['fmtDate','positiveIncreasePopulation'], ascending=False).head(5).iterrows():
    #print(row['state'])
    local_df = report_df.loc[report_df['state'] == row['state']]
    #local_df = report_df.loc([row['state']]))
    loopLabel = row['state'] + " 7 day population infection moving average"
    plt.plot_date(local_df['fmtDate'], (local_df['SMA_7_CasesPerPopulation']), color=colors[counter], linestyle='solid', label=loopLabel)
    counter += 1
plt.grid(b=True, which='both', axis='both')
plt.legend(loc='upper left')
fileName = 'CovidTop5States' + time.strftime("%Y%m%d") + '.pdf'
savePath = os.path.join(reportDir, fileName)
plt.savefig(savePath, dpi=75 )
#plt.show()
plt.close()
