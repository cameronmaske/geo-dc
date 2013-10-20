import json
from models import AirbnbListing
from os import path

def generate_airbnb_geojson(filename="airbnb.geojson"):
    """
    Generate a GEOJSON based on all stored Crime data
    """
    features = []

    # Query for all listings.
    airbnb_listings = AirbnbListing.select()
    for airbnb in airbnb_listings:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates":[airbnb.longitude, airbnb.latitude]},
            "properties": airbnb.as_dict()})

    geojson = {
        "type": "FeatureCollection",
        "features": features}


    directory, _ = path.split(path.abspath(__file__))
    output_directory = directory.replace("data/airbnb", "datasets/airbnb")
    print "{}/{}".format(output_directory, filename)

    with open("{}/{}".format(output_directory, filename),'wb') as outfile:
        json.dump(geojson, outfile)

if __name__ == '__main__':
    generate_airbnb_geojson()
