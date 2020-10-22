from datetime import datetime
from .utils import get_wind_beaufort_description, get_wind_angle_description, kelvin_to_celsius


class WeatherInformation:
    """
    Represents the custom response style
    """

    def __init__(self, data):
        """
        Args:
            data (dict): Dict with the weather information
        """
        self.location_name = data.get('name') + ', ' + data.get('sys').get('country')
        self.temperature = str(round(kelvin_to_celsius(data.get('main').get('temp')), 1)) + ' °C'
        self.wind = get_wind_beaufort_description(data.get('wind').get('speed')) + ', ' + str(data.get('wind').get('speed')) + ' m/s, ' + get_wind_angle_description(data.get('wind').get('speed'))
        self.cloudiness = data.get('weather')[0].get('description')
        self.pressure = str(data.get('main').get('pressure')) + ' hpa'
        self.humidity = str(data.get('main').get('humidity')) + '%'
        self.sunrise = format(datetime.fromtimestamp(data.get('sys').get('sunrise')), '%H:%m')
        self.sunset = format(datetime.fromtimestamp(data.get('sys').get('sunset')), '%H:%m')
        self.geo_coordinates = '[' + str(data.get('coord').get('lon')) + ', ' + str(data.get('coord').get('lat')) + ']'
        self.requested_time = format(data.get('requested_time'), '%Y-%m-%d %H:%M:%S')
        self.forecast = None
