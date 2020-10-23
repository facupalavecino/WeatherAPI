from datetime import datetime
from .utils import get_wind_beaufort_description, get_wind_angle_description


class WeatherInformation:
    """
    Represents the current weather information of a City
    """
    def __init__(self, data=None):
        """
        Args:
            data (dict): Dict with the weather information
        """
        if data is not None:
            self.timestamp = datetime.fromtimestamp(data.get('dt'))
            self.temperature = round(data.get('main').get('temp'), 1)
            self.wind_speed = data.get('wind').get('speed')
            self.wind_deg = data.get('wind').get('deg')
            self.cloudiness = data.get('weather')[0].get('description')
            self.pressure = data.get('main').get('pressure')
            self.humidity = data.get('main').get('humidity')
            self.sunrise = datetime.fromtimestamp(data.get('sys').get('sunrise'))
            self.sunset = datetime.fromtimestamp(data.get('sys').get('sunset'))

    def get_readable(self):
        """ Returns a dict containing the human-readable description of each attribute """
        return {
            'timestamp': format(self.timestamp, '%Y-%m-%d %H:%M'),
            'temperature': str(self.temperature) + ' °C',
            'wind': get_wind_beaufort_description(self.wind_speed) + ', ' + str(
                self.wind_speed) + ' m/s, ' + get_wind_angle_description(self.wind_deg),
            'cloudiness': self.cloudiness,
            'pressure': str(self.pressure) + ' hpa',
            'humidity': str(self.humidity) + '%',
            'sunrise': format(self.sunrise, '%H:%m'),
            'sunset': format(self.sunset, '%H:%m'),
        }


class WeatherForecast(WeatherInformation):
    """
    Represents the forecast weather information of a City
    """
    def __init__(self, data):
        super().__init__()
        self.timestamp = datetime.fromtimestamp(data.get('dt'))
        self.temperature = round((data.get('temp').get('min') + data.get('temp').get('max')) / 2, 2)
        self.wind_speed = data.get('wind_speed')
        self.wind_deg = data.get('wind_deg')
        self.cloudiness = data.get('weather')[0].get('description')
        self.pressure = data.get('pressure')
        self.humidity = data.get('humidity')
        self.sunrise = datetime.fromtimestamp(data.get('sunrise'))
        self.sunset = datetime.fromtimestamp(data.get('sunset'))


class City:
    """ Represents a City or location in the World """
    def __init__(self, data):
        self.name = data.get('name')
        self.country = data.get('sys').get('country')
        self.geo_coordinates = [data.get('coord').get('lat'), data.get('coord').get('lon')]
        self.requested_time = data.get('requested_time')
        self.current_time = WeatherInformation()
        self.forecast = []

    def get_readable(self):
        """
        Returns a dict containing the human-readable description of the City, including the current and forecast information if available
        """
        ret_val = {
            'location_name': self.name + ', ' + self.country,
            'geo_coordinates': '[' + str(self.geo_coordinates[0]) + ', ' + str(self.geo_coordinates[1]) + ']',
            'requested_time': format(self.requested_time, '%Y-%m-%d %H:%M:%S')
        }
        ret_val.update(self.current_time.get_readable())
        ret_val['forecast'] = None
        if len(self.forecast) > 0:
            ret_val['forecast'] = []
            for f in self.forecast:
                ret_val['forecast'].append(f.get_readable())

        return ret_val