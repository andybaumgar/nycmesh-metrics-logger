import requests
import json
from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
import time

from nycmesh_metrics_logger.mesh_utils import nn_from_string, identifier_string_from_string_multi
from nycmesh_metrics_logger.config import devices_endpoint, statistics_endpoint

load_dotenv() 

headers={'x-auth-token': os.environ.get('NYCMESH_TOOL_AUTH_TOKEN')}

def get_uisp_devices():

    response = requests.get(devices_endpoint, headers=headers, verify=False)

    devices = json.loads(response.content)

    if devices == []:
        raise ValueError('Problem downloading UISP devices.')

    return devices

def devices_to_df(devices):
    parsed_devices = []
    for device in devices:
        try:
            name = device['identification']['displayName']
            nn = nn_from_string(name)
            if nn is None:
                continue
            # location = database_client.nn_to_location(nn)
            last_seen = device['overview']['lastSeen']

            row = {
                'name': name,
                'lastSeen':device['overview']['lastSeen'],
                'model':device['identification']['model'],
                'modelName':device['identification']['modelName'],
                'id':device['identification']['id'],
                'nn': nn,
                'ip':device['ipAddress'],
                'frequency': device['overview']['frequency'],
                'has60GhzRadio': device['features']['has60GhzRadio'],
                'site_name': device['identification']['site']['name']
            }

            parsed_devices.append(row)
        except (KeyError, TypeError):
            continue
    
    df = pd.DataFrame.from_dict(parsed_devices)
    return df

def filter_unique_links(df):

    df['node_1'] = df['name'].apply(lambda x: identifier_string_from_string_multi(x, position=0))
    df['node_2'] = df['name'].apply(lambda x: identifier_string_from_string_multi(x, position=1))

    df['link'] = df['node_1'] + '-' + df['node_2']
    
    df = df.sort_values(by=['node_1'])
    df = df.drop_duplicates(subset=['link'], keep='first')
    return df

def get_device_history(device_id):
    # Available interval values : hour, fourhours, day, week, month, quarter, year, range
    
    endpoint = statistics_endpoint.format(device_id)
    params = {
    # "start":int(time.time() * 1000),
    # "period":int(11*60*1000),
    "interval": "hour",
    }
    response = requests.get(endpoint, headers=headers, params=params, verify=False)
    history = json.loads(response.content)
    return history


if __name__ == "__main__":
    device_id = '673cb9d4-7365-4714-8129-1c38cd697988'
    history = get_device_history(device_id)

