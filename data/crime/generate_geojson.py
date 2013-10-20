import json
from models import Crime

def generate_crime_geojson():
    """
    Generate a GEOJSON based on all stored Crime data
    """
    # Get all crimes in db.
    crimes = Crime.select()
    features = []

    for crime in crimes:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates":[crime.longitude, crime.latitude]},
            "properties": {
                "offense": crime.offense,
                "method": crime.method,
                "shift": crime.shift,
                "reported": crime.reported,
                "address": crime.block_address,
                "y": crime.block_y,
                "x": crime.block_x}})

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('crime.geojson', 'wb') as outfile:
        json.dump(geojson, outfile)

if __name__ == '__main__':
    generate_crime_geojson()
