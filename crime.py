import csv
import requests
import xmltodict
import json
from collections import OrderedDict

def find(key, value):
  for k, v in value.iteritems():
    if k == key:
      yield v
    elif isinstance(v, dict) or isinstance(v, OrderedDict):
      for result in find(key, v):
        yield result
    elif isinstance(v, list):
      for d in v:
        for result in find(key, d):
          yield result

csv_file = csv.DictReader(open('crime.csv', 'rb'))

features = []

for row in csv_file:
    url = "http://citizenatlas.dc.gov/newwebservices/locationverifier.asmx/findLocation"
    params = {"str": row['BLOCKSITEADDRESS']}
    response = requests.get(url, params=params)
    doc = xmltodict.parse(response.content)
    try:
        lat = find('LATITUDE', doc)
        lng = find('LONGITUDE', doc)
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates":[
                    lat, lng],
                "properties": {
                    "offense": row["OFFENSE"],
                    "shift": row["SHIFT"],
                    "time": row["REPORTDATETIME"]
                }}})
        print lat, lng
    except:
        print response.content

geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open('crime.geojson', 'w') as outfile:
    json.dump(geojson, outfile)