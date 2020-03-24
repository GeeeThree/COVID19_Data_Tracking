#All data regarding COVID-19 can be found at https://github.com/CSSEGISandData/COVID-19
#Data sources from John Hopkins, WHO, CDC, ECDC, NHC, DXY, 1point3acres, Worldometers.info, BNO, 
#state and national government health departments, and local media reports. 

import requests
import csv
from tabulate import tabulate
import datetime
import pandas as pd
from pandas import DataFrame
import time

import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

data_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
file_location = "/home/g3/covidfiles/"
filename = time.strftime('%m-%d-%Y.csv')
times = time.strftime('%m-%d-%Y')

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
df3 = DataFrame(df2, columns = ['FIPS', 'Admin2', 'Province_State', 'Country_region', 'Last_Update', 'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'Combined_Key'])
select_col = df3.loc[df3['Admin2'] == 'Miami-Dade']
print(select_col.values[0])

MiamiDade = select_col.values[0]
df4 = DataFrame(MiamiDade)
case = df4.iloc[7].iloc[-1]
death = df4.iloc[8].iloc[-1]
rec = df4.iloc[9].iloc[-1]
active = df4.iloc[10].iloc[-1]

pop = 2752000
prev_cases = int(rows)
cases = int(case)
deaths = int(death)
recover = int(rec)
still_active = int(active)

results = [(times, cases, still_active, cases - prev_cases, deaths, recover, cases/pop*100, deaths/cases*100)]

with open(file_location+filename2, "a") as update_file:
	update_file.write(tabulate(results, headers = ['                 ', '           ', '            ', '              ', '            ', '               ', '                                     ', '                    '], tablefmt='plain'))
print(tabulate(results, headers = ['                 ', '           ', '            ', '              ', '            ', '               ', '                                     ', '                    '], tablefmt='plain'))

fromaddr = "example@gmail.com"
toaddr = ['example@gmail.com','example2@gmail.com']

msg = MIMEMultipart()
msg['From'] = fromaddr 
msg['To'] = ', '.join(toaddr)
msg['Subject'] = "COVID19 Data Updates"
body = "These are the COVID19 Data updates for Florida from 03-10-2020 through 03-23-2020 and the COVID19 Data updates for Miami-Dade County from 03-23-2020 through "+times
msg.attach(MIMEText(body, 'plain'))
filename3 = "/home/g3/covidfiles/COVID19_Stats.txt"
attachment = open(filename3, "rb") 
p = MIMEBase('application', 'octet-stream')
p.set_payload((attachment).read())
encoders.encode_base64(p) 
p.add_header('Content-Disposition', "attachment; filename= %s" % 'COVID-19_Florida_Updates.txt')
msg.attach(p) 
s = smtplib.SMTP('smtp.gmail.com', 587) 
s.starttls()
s.login(fromaddr, "Password")
text = msg.as_string() 
s.sendmail(fromaddr, toaddr, text)
time.sleep(10)
s.quit()
