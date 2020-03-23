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
filename = time.strftime('%m-22-%Y.csv')
times = time.strftime('%m-22-%Y')

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
rows = df.iloc[-2].iloc[1] #previous day data
df2 = pd.read_csv(file_location+filename, sep=',') #current day data
df3 = DataFrame(df2, columns = ['Province/State', 'Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered', 'Latitude', 'Longitude'])
select_col = df3.loc[df3['Province/State'] == 'Florida']

Florida = select_col.values[0]
df4 = DataFrame(Florida)
case = df4.iloc[3].iloc[-1]
death = df4.iloc[4].iloc[-1]
rec = df4.iloc[5].iloc[-1]

pop = 21300000
prev_cases = int(rows)
cases = int(case)
deaths = int(death)
recover = int(rec)

results = [(times, cases, cases - prev_cases, deaths, recover, cases/pop*100, deaths/cases*100)]

with open(file_location+filename2, "a") as update_file:
	update_file.write(tabulate(results, headers = ['       ', '           ', '              ', '            ', '               ','                                ', '                                      '], tablefmt='plain'))

print(tabulate(results))

fromaddr = "example@gmail.com"
toaddr = ['example@gmail.com', 'example2@gmail.com']

msg = MIMEMultipart()
msg['From'] = fromaddr 
msg['To'] = ', '.join(toaddr)
msg['Subject'] = "COVID19 Data Updates"
body = "These are the COVID19 Data updates for Florida on "+times
msg.attach(MIMEText(body, 'plain'))
filename3 = "/home/g3/covidfiles/COVID19_Stats.txt"
attachment = open(filename3, "rb") 
p = MIMEBase('application', 'octet-stream')
p.set_payload((attachment).read())
encoders.encode_base64(p) 
p.add_header('Content-Disposition', "attachment; filename= %s" % filename3)
msg.attach(p) 
s = smtplib.SMTP('smtp.gmail.com', 587) 
s.starttls()
s.login(fromaddr, "Password")
text = msg.as_string() 
s.sendmail(fromaddr, toaddr, text)
s.quit()

