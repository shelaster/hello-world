import sys
import urllib.request, urllib.error, urllib.parse
import json
url = urllib.request.urlopen("http://api.gios.gov.pl/pjp-api/rest/station/findAll").read()
data = json.loads(url)
station_ids = []
station_names = []
sensor_ids = []
#get all station IDs in given city
print("Stacje znalezionie w mieście " + sys.argv[1])
for d in data:
    if d['city']['name'] == sys.argv[1]:
        station_ids.append(d['id'])
        station_names.append(d['stationName'])
        


station_ids = list(map(str, station_ids))


for s in range(len(station_ids)):
    url = ("http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/", station_ids[s])
    url = "".join(url)
    qualIndex=json.loads(urllib.request.urlopen(url).read())
    
    print("\n\t" + station_names[s] + " -- Indeks jakości powietrza: " + qualIndex['stIndexLevel']['indexLevelName'])

    url = ("http://api.gios.gov.pl/pjp-api/rest/station/sensors/", station_ids[s])
    url = "".join(url)
    sensor_list=json.loads(urllib.request.urlopen(url).read())
    for d in range(len(sensor_list)):
        sensor_ids.append(sensor_list[d]['id'])
    sensor_ids = list(map(str, sensor_ids))
    for x in range(len(sensor_ids)):
        i = 0
        url = ("http://api.gios.gov.pl/pjp-api/rest/data/getData/", sensor_ids[x])
        url = "".join(url)
        data=json.loads(urllib.request.urlopen(url).read())
        while data['values'][i]['value'] == None:
            i += 1
        j = i+1
        while data['values'][j]['value'] == None:
            j += 1
        percentage = (data['values'][i]['value'] - data['values'][j]['value'])/(abs(data['values'][j]['value'])/100)
        print(data['key'] +": " + str(data['values'][i]['value']) + " poprzedni odczyt: " + str(data['values'][j]['value']) + " zmiana o: " + "{:3.2f}".format(percentage)  +"%")
    sensor_ids = []
