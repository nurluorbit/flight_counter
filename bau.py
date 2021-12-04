from bs4 import BeautifulSoup
import requests, json, time
from datetime import date, timedelta

dictionary = {"Jan":"Oca", "Feb":"Şub", "Mar":"Mar", "Apr":"Nis", "May":"May", "Jun":"Haz", "Jul":"Tem", "Aug":"Ağu", "Sep":"Eyl", "Oct":"Eki", "Nov":"Kas", "Dec":"Ara"}

_date1 = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
_date = (date.today() - timedelta(days=1)).strftime('%d-%b-%Y')

jsonfile = open(f"./BAU.json",)
data = json.load(jsonfile) 
datas = []

for j in data["BAU"]:
    site = requests.get(f"https://flightaware.com/live/flight/{j}/history")
    sitecontent = BeautifulSoup(site.text)
    sitedate = sitecontent.find_all("td",attrs={'class':'nowrap'})
    x = 0
    for i in sitedate:
        seperation = i.a.text.split("-")
        english = False
        turkish = False
        for v in dictionary:
            if (seperation[1] == v):
                english = True
            elif (seperation[1] == dictionary[f"{v}"]):
                turkish = True
            if (turkish == True or english == True):
                index = f"{v}"
                break
        if (english == True):
            _date = _date.split("-")
            _date[1] = index
            _date = "-".join(_date)
        elif (turkish == True):
            _date = _date.split("-")
            _date[1] = dictionary[index]
            _date = "-".join(_date)
        if (i.a.text == _date):
            x+=1
    print(f"{j} = {x}")
    datas.append(f"{j} , {x}")

filename = f'/tmp/flights-{_date1}.csv'
with open(filename, 'a') as f:
    for k in datas:
        f.write(f"{k} \n")
