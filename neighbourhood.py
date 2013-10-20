import requests
import json
from models import AirbnbListing
from utils import get_logger

logger = get_logger()

def create_geojson():
    features = []
    unique_neighborhoods = []
    airbnb_listings = AirbnbListing.select()

    for listing in airbnb_listings:
        if listing.neighbourhood not in unique_neighborhoods:
            unique_neighborhoods.append(listing.neighbourhood)

    for neighborhood_id in unique_neighborhoods:
        response = requests.get("https://www.airbnb.co.uk/locations/neighborhoods/{}".format(neighborhood_id))
        json_url = response.url + '.json'
        logger.info(json_url)
        json_response = requests.get(json_url).json()
        features.append({
            "type": "Feature",
            "geometry": json_response['neighborhood']['bounds'],
            "properties": {
                "name": json_response['neighborhood']['name']
            }})

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('neighborhood.geojson', 'w') as outfile:
        json.dump(geojson, outfile)

if __name__ == '__main__':
    create_geojson()
