import requests
import json
import csv
from bs4 import BeautifulSoup

def find_crime():
    features = []
    limit = 50
    count = 0

    url = "http://citizenatlas.dc.gov/newwebservices/locationverifier.asmx/findLocation"

    csv_file = csv.DictReader(open('crime.csv', 'rb'))

    for row in csv_file:
        if count > limit:
            break
        count += 1
        try:
            params = {"str": row['BLOCKSITEADDRESS']}
            response = requests.get(url, params=params)
            soup = BeautifulSoup(response.content)
            cords = {
                'lat': soup.findAll('latitude')[0].text,
                'lng': soup.findAll('longitude')[0].text
            }

            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates":[cords['lat'], cords['lng']],
                    "properties": {
                        "offense": row["OFFENSE"],
                        "shift": row["SHIFT"],
                        "time": row["REPORTDATETIME"]
                    }}})
            print cords
        except Exception as e:
            print "Failed for {} due to {}".format(row['BLOCKSITEADDRESS'], e)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('crime.geojson', 'w') as outfile:
        json.dump(geojson, outfile)

if __name__ == '__main__':
    find_crime()
