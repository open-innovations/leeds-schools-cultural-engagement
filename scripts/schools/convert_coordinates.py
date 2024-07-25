import os 
import pandas as pd 
import json
from shapely.geometry import shape

GEOJSON_DATA = os.path.join('src', '_data', 'viz', 'schools', 'school-map.geojson')

geojson_data = pd.read_json(GEOJSON_DATA)
OUT_DIR = os.path.join('src', '_data', 'viz', 'schools')

def calculate_coords(geojson_data):
    features = geojson_data['features']
    centroid_features = []

    for feature in features:
        geometry = feature['geometry']
        geom_type = geometry['type']
        coordinates = geometry['coordinates']

        if geom_type == 'Polygon':
            polygon = shape({'type': 'Polygon', 'coordinates': coordinates})
            centroid = polygon.centroid
            centroid_coordinates = [centroid.x, centroid.y]

        elif geom_type == 'MultiPolygon':
            multipolygon = shape({'type': 'MultiPolygon', 'coordinates': coordinates})
            centroid = multipolygon.centroid
            centroid_coordinates = [centroid.x, centroid.y]

        centroid_features.append({
            'type': 'Feature',
            'properties': feature['properties'],
            'geometry': {
                'type': 'Point',
                'coordinates': centroid_coordinates
            }
        })

    return {
        'type': 'FeatureCollection',
        'features': centroid_features
    }

if __name__ == '__main__':


    centroid_data = calculate_coords(geojson_data)
    with open(os.path.join(OUT_DIR, 'schools_map_centroid.geojson'), 'w') as f:
        json.dump(centroid_data, f, indent=2)