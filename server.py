from flask import Flask, render_template, request, redirect
from datetime import datetime
import csv
import bs4
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
import os

states = os.path.join('data', 'countries.geojson')
unemployement_data = os.path.join('data', 'map_co.csv')
state_data = pd.read_csv(unemployement_data)

m = folium.Map(location=[48, 0], zoom_start=2)

m.choropleth(
    geo_data=states,
    name='choropleth',
    data=state_data,
    columns=['Country', 'Cases'],
    key_on='feature.id',
    # threshold_scale = [0,1000,100000,500000,2000000],
    range_color=[1,50000], 
    fill_color='YlGn',
    # color_continuous_scale='blues',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Corona Cases Rate %'
)

folium.LayerControl().add_to(m)
m.save('./templates/map.html')

# Confirmed Cases
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
c_cols = confirmed_df.keys()
confirmed = confirmed_df.loc[:, c_cols[4]:c_cols[-1]]
last_date1 = confirmed_df.loc[:, c_cols[-1]:c_cols[-1]]
cc = last_date1.keys().max()
total_cases = confirmed_df[cc].sum()

# Death Cases
deaths_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
d_cols = deaths_df.keys()
deaths = deaths_df.loc[:, d_cols[4]:d_cols[-1]]
last_date2 = confirmed_df.loc[:, c_cols[-1]:c_cols[-1]]
dd = last_date2.keys().max()
total_deaths = deaths_df[dd].sum()

# Countries affected
country = confirmed_df.groupby('Country/Region')["Country/Region"].sum()
affected_countries = country.count()

# Another dataset
# path = 'https://raw.githubusercontent.com/umangkejriwal1122/Machine-Learning/master/Data%20Sets/covid_19_clean_complete.csv'
# data = pd.read_csv(path)
# total_case = data['Confirmed'].sum()

# previous = datetime.datetime.today() - datetime.timedelta(days=1)
date = datetime.now().strftime("%d %B %Y")
time = datetime.now().strftime("%I:%M:%p")

recoveries_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
confirmed_df.drop(['Province/State'], axis=1, inplace=True)
deaths_df.drop(['Province/State'], axis=1, inplace=True)
recoveries_df.drop(['Province/State'], axis=1, inplace=True)

c_cols = confirmed_df.keys()
d_cols = deaths_df.keys()
r_cols = recoveries_df.keys()

x = confirmed_df.groupby('Country/Region')["Country/Region","Lat","Long",c_cols[-1]].sum()
y = deaths_df.groupby('Country/Region')["Country/Region","Lat","Long",d_cols[-1]].sum()
z = recoveries_df.groupby('Country/Region')["Country/Region","Lat","Long",r_cols[-1]].sum()

case = x[c_cols[-1]]
dead = y[d_cols[-1]]
recover = z[r_cols[-1]]
co_name = x.index
active = case-dead-recover

listw=[]
for i in range(188):
  listw.append([co_name[i],case[i],dead[i],recover[i],active[i]])

page = requests.get("https://news.search.yahoo.com/search;_ylt=AwrXgCNS191eqQwAWEXQtDMD;_ylc=X1MDNTM3MjAyNzIEX3IDMgRmcgNtY2FmZWUEZnIyA3NiLXRvcARncHJpZAM4Unl4aXk1Z1JpV1hQR1R5d0tDRzNBBG5fcnNsdAMwBG5fc3VnZwM4BG9yaWdpbgNuZXdzLnNlYXJjaC55YWhvby5jb20EcG9zAzAEcHFzdHIDBHBxc3RybAMwBHFzdHJsAzIwBHF1ZXJ5A2NvdmlkJTIwMTklMjBsYXRlc3QlMjBuZXdzBHRfc3RtcAMxNTkxNTk2OTE0?p=covid+19+latest+news&fr2=sb-top&fr=mcafee&guce_referrer=aHR0cHM6Ly9uZXdzLnNlYXJjaC55YWhvby5jb20v&guce_referrer_sig=AQAAAD9LsNQV_G4AcaMzD7PVp777ZPPWTX1BMBQ5a94qy_DTpB0gEG71oupmO3_2QiFK2AsTPf1L2P9TS5xYnmZQG4w6XiADUC6KGStKcw7qVkplDnxeMHxiKurt9IKiIK2gCFun3Mhj1W2lzQKr2RsLNGRlPjiRJmyNQbH786wTaG5A&_guc_consent_skip=1591596945")
soup = BeautifulSoup(page.content,'html.parser')
a = soup.find('ol',class_='mb-15 reg searchCenterMiddle')
b = a.find_all(class_='dd NewsArticle')

news_image = []

for l in range(len(b)):
    try:
        news_image.append(b[l].find('img', class_="s-img")['data-src'])    
    except:
        l=l+1;

    
# news_link = []
# for k in range(len(b)):
#     link_a = b[k].find('a')
#     news_link.append(link_a['href'])

# news_heading = []
# for i in range(len(b)):
#     news_heading.append(b[i].find(class_='fz-16 lh-20').text)

# news_text = []
# for j in range(len(b)):
#     news_text.append(b[j].find('p').text) 

# subtitle1 = []
# for o in range(len(b)):
#     subtitle1.append(b[o].find('span', class_="mr-5 cite-co").text)

# subtitle2 = []
# for p in range(len(b)):
#     subtitle2.append(b[p].find('span', class_="fc-2nd mr-8").text)

@app.route('/')
def index():
    return render_template('./index.html', total_cases=total_cases, total_deaths=total_deaths, affected_countries=affected_countries, time=time, date=date, listw=listw)

# @app.route('/test')
# def chart():
# 	plt.plot(first,second)
# 	plt.savefig("./static/img/my_fig.png", transparent=True)
# 	return render_template('untitled1.html', name=plt.show())

@app.route('/index.html')
def overview():
    return render_template('./index.html', total_cases=total_cases, total_deaths=total_deaths, affected_countries=affected_countries, time=time, date=date, listw=listw)

@app.route('/habits.html')
def habits():
    return render_template('./habits.html')

@app.route('/prevention.html')
def prevention():
    return render_template('./prevention.html')

@app.route('/symptoms.html')
def symptoms():
    return render_template('./symptoms.html')

@app.route('/news.html')
def news():
    return render_template('./news.html')

def write_to_file(data):
	with open('database.txt', mode='a') as database:
		name = data["name"]
		email = data["email"]
		file = database.write(f'\n{name},{email}')

def write_to_csv(data):
	with open('database.csv',newline='', mode='a') as database2:
		name = data["name"]
		email = data["email"]
		msg = data["msg"]
		csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow([name,email,msg])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
    	try:
    		data = request.form.to_dict()
    		write_to_csv(data)
    		return redirect('/index.html')
    	except:
    		return 'did not save to database'
    else:
   		return 'something went wrong. Try again!'
