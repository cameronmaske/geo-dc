import json

features = []

# south to north
start_lat = 38.856
# west to east
start_lon = -77.15
increment = 0.010
span_lon = 24
span_lat = 14

for i in range(span_lon):
    cur_lon = start_lon + (increment * i)
    for n in range(span_lat):
        cur_lat = start_lat + (increment * n)
        polygon = {
            "type": "Polygon",
            "coordinates": [[
                [cur_lon, cur_lat],
                [cur_lon + increment, cur_lat],
                [cur_lon + increment, cur_lat + increment],
                [cur_lon, cur_lat + increment],
            ]]
        }
        features.append({
            "type":"Feature",
            "geometry": polygon,
            "properties": {
                "name": "{}-{}".format(i, n),
            }})


geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open('squares.geojson', 'w') as outfile:
    json.dump(geojson, outfile)