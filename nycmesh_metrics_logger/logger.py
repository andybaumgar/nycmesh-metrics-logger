# %%
import pandas as pd
from datetime import date
import itertools
from influxdb import InfluxDBClient
from datetime import datetime
import os
import datetime
import time
import pickle

import nycmesh_metrics_logger.config as config
from nycmesh_metrics_logger.uisp_client import (
    devices_to_df,
    get_device_history,
    get_uisp_devices,
    filter_unique_links,
)

from open_weather_map import get_weather_data

influx_client = InfluxDBClient(
    os.environ.get("DATABASE_HOST"),
    8086,
    username=os.environ.get("DATABASE_USERNAME"),
    password=os.environ.get("DATABASE_PASSWORD"),
    database=config.database,
)


def is_24_ghz(history):
    return "af24" in history["name"].lower()


def get_main_interface(history):
    if is_24_ghz(history):
        for interface in history["interfaces"]:
            if interface["id"] == "wlan":
                return interface

    # 60Ghz
    for interface in history["interfaces"]:
        if interface["id"] == "main":
            return interface


def filter_60_and_24_ghz(df: pd.DataFrame):
    df = df[
        (df["has60GhzRadio"] == True) | (df["name"].str.contains("af24", case=False))
    ]
    return df


def get_device_histories(device_limit=None):
    devices = get_uisp_devices()
    df = devices_to_df(devices)
    # df = df[df['name']=='nycmesh-231-AF60HD-333']

    df = filter_60_and_24_ghz(df)
    df = filter_unique_links(df)
    if device_limit is not None:
        df = df.head(device_limit)

    histories = []

    for device_id, device_name in zip(df["id"], df["name"]):
        history = get_device_history(device_id)

        history["name"] = device_name
        histories.append(history)

    return histories


def create_device_metrics(history):
    # only get more recent (last) element
    measurements = get_main_interface(history)["transmit"]
    number_of_measurements = 5
    if len(measurements) >= number_of_measurements:
        last_measurements = measurements[-number_of_measurements:]
    else:
        last_measurements = measurements

    points = []
    for measurement in last_measurements:
        utc_time = datetime.datetime.utcfromtimestamp(measurement["x"] / 1000)
        formatted_time = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        if measurement["y"] is None:
            continue

        point = {
            "measurement": "devices",
            "time": formatted_time,
            "tags": {
                "name": history["name"],
            },
            "fields": {"outage": 1 if measurement["y"] == 0 else 0},
        }

        points.append(point)

    return points


def log_devices(histories):
    print(f"Loaded {len(histories)} histories")

    # get flat timeseries for all devices
    nested_metrics = []
    for history in histories:
        try:
            nested_metrics.append(create_device_metrics(history))
        except Exception as e:
            print(f'Error creating metrics for {history["name"]}: {e}')
            pass

    metrics = list(itertools.chain.from_iterable(nested_metrics))

    influx_client.write_points(metrics)


def log_precipitation():
    weather_data = get_weather_data()
    utc_time = datetime.datetime.utcnow()
    formatted_time = utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    point = {
        "measurement": "precipitation",
        "time": formatted_time,
        "fields": {
            "volume": weather_data["precipitation_volume"],
            "wind_speed": weather_data["wind_speed"],
            "wind_gust": weather_data["wind_gust"],
        },
    }

    influx_client.write_points([point])


def run():
    while True:
        print("logger running")
        histories = get_device_histories()
        log_devices(histories)
        print("logged devices")

        log_precipitation()

        time.sleep(60 * 5)


if __name__ == "__main__":
    # save_history_filename = 'histories.pkl'
    histories = get_device_histories()
    # with open(save_history_filename, 'wb') as pickle_file:
    #         pickle.dump(histories, pickle_file)

    # with open(save_history_filename, 'rb') as pickle_file:
    #         histories = pickle.load(pickle_file)

    log_devices(histories)

    # log_precipitation()
