from nycmesh_metrics_logger.open_weather_map import get_weather_data


def test_get_weather_data():
    data = get_weather_data()
    assert data is not None
