import requests
import csv
from tabulate import tabulate
import datetime
import pandas as pd
from pandas import DataFrame
import time


data_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
file_location = "/home/g3/covidfiles/"
filename = time.strftime('%m-%d-%Y.csv')

r = requests.get(data_url+filename)
if(r.status_code != 200):
    print("Failure\n")
    exit()
else:
    with open(file_location+filename,'wb') as f:
        f.write(r.content)
    print("Success")

filename2 = "COVID19_Stats.txt"
df = pd.read_csv(file_location+filename2, delim_whitespace=True)
rows = df.iloc[-1].iloc[1] #previous day data
df2 = pd.read_csv(file_location+filename, sep=',') #current day data
df3 = DataFrame(df2, columns = ['Province/State', 'Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered', 'Latitude', 'Longitude'])
select_col = df3.loc[df3['Province/State'] == 'Florida']

Florida = select_col.values[0]
df4 = DataFrame(Florida)
case = df4.iloc[3].iloc[-1]
death = df4.iloc[4].iloc[-1]
rec = df4.iloc[5].iloc[-1]
print(case)

pop = 21300000
prev_cases = int(rows)
cases = int(case)
deaths = int(death)
recover = int(rec)

results = [(filename, cases, cases - prev_cases, deaths, recover, cases/pop*100, deaths/cases*100)]

with open(file_location+filename2, "a") as update_file:
	update_file.write(tabulate(results, headers = ["Florida", "Total_Cases", "Rate_of_Change", "Total Deaths", "Total Recovered", "Percentage of Population Infected", "Percentage of Deaths from Total Cases"]))

#print(tabulate(results, headers = ["Florida", "Total_Cases", "Rate_of_Change", "Total Deaths", "Total Recovered", "Percentage of Population Infected", "Percentage of Deaths from Total Cases"]))


