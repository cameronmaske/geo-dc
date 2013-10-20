import requests
import json
from settings import GOOGLE_API_KEY
from time import sleep


def create_geojson():
    # Console: https://code.google.com/apis/console/b/0/#project:845810689195:stats:places_backend
    # 1k limit per day
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    numbers = range(1, 50)
    streets = []
    cardinals = ["NW", "NE"]

    for cardinal in cardinals:
        for number in numbers:
            query = "{} Street {}, Washington, D.C., District of Columbia".format(number, cardinal)
            print query

            params = {
                "query": query,
                "sensor": "true",
                "key": GOOGLE_API_KEY
            }
            json_response = requests.get(url, params=params).json()
            try:
                location = json_response['results'][0]['geometry']['location']
                print location
                streets.append({
                    'address': json_response['results'][0]['formatted_address'],
                    'location':location})
            except:
                pass
            # Slow requests due to API limits. Annoying!
            sleep(3)

    lng = sorted([s['location']['lng'] for s in streets])
    range_lng = float(max(lng)) - min(lng)
    avg_lng_inc = range_lng / float(len(lng))
    start_lat = 38.813
    end_lat = 39.0135
    streets = sorted(streets, key=lambda s: s['location']['lng'])

    features = []
    for index, street in enumerate(streets):
        try:
            next_street = streets[index + 1]
        except:
            break
        lat = start_lat
        while lat <= end_lat:
            next_lat = lat + avg_lng_inc
            polygon = {
                "type": "Polygon",
                "coordinates": [[
                    [street['location']['lng'], lat],
                    [next_street['location']['lng'], lat],
                    [next_street['location']['lng'], next_lat],
                    [street['location']['lng'], next_lat],
                ]]
            }
            features.append({
                "type":"Feature",
                "geometry": polygon,
                "properties": {
                    "name": "{}-{}".format(street['address'], lat),
                }})
            lat = next_lat

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('streets.geojson', 'w') as outfile:
        json.dump(geojson, outfile)

if __name__ == '__main__':
    create_geojson()
