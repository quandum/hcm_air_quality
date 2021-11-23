
import os, sys, platform
import csv,json
from pprint import pprint

CURRENT_WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
# CURRENT_WORKING_DIRECTORY = r'd:\HCMUS\Data Engineer\project'
DATA_DIRECTORY = os.path.join(CURRENT_WORKING_DIRECTORY,'data')



f=open(os.path.join(DATA_DIRECTORY,'locations_link.csv'),'r',encoding='utf8')
reader=csv.DictReader(f)
location_data=[dict(x) for x in reader]
f.close()
pprint(location_data)


# In[19]:


hourly_data_csv=open(os.path.join(DATA_DIRECTORY,'hourly_data.csv'),'w',encoding='utf8')
writer=csv.DictWriter(hourly_data_csv,fieldnames=['station','timestamp','aqi','rating_aqi','pm2.5','rating_pm2.5'])
writer.writeheader()
for location in location_data:
    station=location['location']
    station_directory=os.path.join(DATA_DIRECTORY,location['vn_no_accent'])
    aqi=[dict(x) for  x in csv.DictReader(open(os.path.join(station_directory,'aqihourly.csv'),'r',encoding='utf8'))]
    pm25=[dict(x) for  x in csv.DictReader(open(os.path.join(station_directory,'pm2.5hourly.csv'),'r',encoding='utf8'))]
    data=[]
    for rec in aqi:
        data.append({
            'station':station,
            'timestamp':rec['timestamp'],
            'aqi':rec['value'],
            'rating_aqi':rec['rating'],
            'pm2.5':'',
            'rating_pm2.5':''
        })
    for rec in pm25:
        ts=rec['timestamp']
        existed=False
        for i in range(len(data)):
            if (data[i]['timestamp']==ts):
                existed=True
                data[i]['pm2.5']=rec['value']
                data[i]['rating_pm2.5']=rec['rating']
        if (existed==False):
            data.append({
                'station':station,
                'timestamp':rec['timestamp'],
                'aqi':'',
                'rating_aqi':'',
                'pm2.5':rec['value'],
                'rating_pm2.5':rec['rating']
            })
    for row in data:
        row['timestamp']=row['timestamp'].replace(',',' 2021,')
        writer.writerow(row)
        
hourly_data_csv.close() 


daily_data_csv=open(os.path.join(DATA_DIRECTORY,'daily_data.csv'),'w',encoding='utf8')
writer=csv.DictWriter(daily_data_csv,fieldnames=['station','date','aqi','rating_aqi','pm2.5','rating_pm2.5'])
writer.writeheader()
for location in location_data:
    station=location['location']
    station_directory=os.path.join(DATA_DIRECTORY,location['vn_no_accent'])
    aqi=[dict(x) for  x in csv.DictReader(open(os.path.join(station_directory,'aqidaily.csv'),'r',encoding='utf8'))]
    pm25=[dict(x) for  x in csv.DictReader(open(os.path.join(station_directory,'pm2.5daily.csv'),'r',encoding='utf8'))]
    data=[]
    for rec in aqi:
        data.append({
            'station':station,
            'date':rec['timestamp'],
            'aqi':rec['value'],
            'rating_aqi':rec['rating'],
            'pm2.5':'',
            'rating_pm2.5':''
        })
    for rec in pm25:
        ts=rec['timestamp']
        existed=False
        for i in range(len(data)):
            if (data[i]['date']==ts):
                existed=True
                data[i]['pm2.5']=rec['value']
                data[i]['rating_pm2.5']=rec['rating']
        if (existed==False):
            data.append({
                'station':station,
                'timestamp':rec['timestamp'],
                'aqi':'',
                'rating_aqi':'',
                'pm2.5':rec['value'],
                'rating_pm2.5':rec['rating']
            })
    for row in data:
        row['date']=row['date']+" 2021"
        writer.writerow(row)
        
daily_data_csv.close() 

print('MERGED DONE!')