import requests
from dotenv import load_dotenv
import os

load_dotenv()


def get_weather_data():
    api_key = os.environ.get("OPEN_WEATHER_MAP_API_KEY")
    city_name = "New York"

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    )

    response = requests.get(url)
    data = response.json()

    if "rain" in data:
        precipitation_volume = data["rain"].get("1h")
    elif "snow" in data:
        precipitation_volume = data["snow"].get("1h")
    else:
        precipitation_volume = 0.0

    if "wind" in data:
        wind_speed = data["wind"]["speed"]
        wind_gust = data["wind"]["gust"]
    else:
        wind_speed = 0.0
        wind_gust = 0.0

    return {
        "precipitation_volume": precipitation_volume,
        "wind_speed": wind_speed,
        "wind_gust": wind_gust,
    }
