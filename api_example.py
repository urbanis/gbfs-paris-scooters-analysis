import requests
import json
import time

# https://github.com/MobilityData/gbfs/blob/master/gbfs.md
# https://data.lime.bike/api/partners/v2/gbfs/paris/gbfs.json

TRANSPORT_DATA_GOUV_FR_BASE_URL = "https://data.lime.bike/api/partners/v2/gbfs/paris/"
TRANSPORT_DATA_GOUV_FR_DATA = {
    "free_bike_status":{ "path": "free_bike_status", "object_name": "bike" },
    "vehicle_types": { "path": "vehicle_types", "object_name": "vehicle_type" },
}

def build_transport_data_gouv_fr_url(data):
    return TRANSPORT_DATA_GOUV_FR_BASE_URL+data["path"]

def print_objects(url, object_name, path):
    current_datetime = time.strftime("%Y%m%d_%H%M")
    
    response = requests.get(url)

    body = response.json()
    array = body["data"][object_name + "s"]
    
    name = path[:-5] + "_" + current_datetime + path[-5:]

    with open(name,'w') as json_file:
        json.dump(array, json_file)

# Collect data from GBFS
free_bike_status_data = TRANSPORT_DATA_GOUV_FR_DATA["free_bike_status"]
free_bike_status_url = build_transport_data_gouv_fr_url(free_bike_status_data)

print_objects(free_bike_status_url, free_bike_status_data["object_name"], '.\gbfsparis.json')