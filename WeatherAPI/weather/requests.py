import requests
from django.conf import settings
from .models import WeatherForecast, WeatherInformation, City


def get_weather_data(city, country, timestamp=None):
    """
    Returns a City with its weather information fetched from an external API

    Args:
        city (str): Name of the city
        country (str): Country code
        timestamp (datetime): Timestamp that represents the moment the information is requested
    Returns:
        City
    Raises:
        Exception: If the request's status code is not 200 (OK)
    """
    owm_api_key = settings.OWM_API.get('KEY')
    owm_api_url = settings.OWM_API.get('BASE_URL')
    owm_api_units = settings.OWM_API.get('UNITS')

    params = {
        'q': city + ',' + country,
        'units': owm_api_units,
        'appid': owm_api_key
    }
    req = requests.get(f"{owm_api_url}/weather", params=params)

    if req.status_code == 200:
        req_data = req.json()
        if timestamp is not None:
            req_data['requested_time'] = timestamp

        city = City(req_data)
        city.current_time = WeatherInformation(req_data)
        return city

    raise Exception("Something went wrong getting the data", req)


def get_forecast_data(city, country, days, timestamp=None):
    """
    Performs an http request to the OWM API and gets weather data for a city

    Args:
        city (str): Name of the city
        country (str): Country code
        days (int): days to include in forecast
        timestamp (datetime): Timestamp that represents the moment the information is requested
    """
    owm_api_key = settings.OWM_API.get('KEY')
    owm_api_url = settings.OWM_API.get('BASE_URL')
    owm_api_exclude = settings.OWM_API.get('PARTS_TO_EXCLUDE')
    owm_api_units = settings.OWM_API.get('UNITS')

    city = get_weather_data(city, country, timestamp)

    if days > 0:
        params = {
            'lat': city.geo_coordinates[0],
            'lon': city.geo_coordinates[1],
            'exclude': owm_api_exclude,
            'units': owm_api_units,
            'appid': owm_api_key
        }

        req = requests.get(f"{owm_api_url}/onecall", params=params)

        if req.status_code == 200:
            data = req.json()
            for i in range(1, days+1):
                city.forecast.append(WeatherForecast(data.get('daily')[i]))
        else:
            print(req.json())
    return city
