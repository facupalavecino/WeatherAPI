def get_cache_key(city, country, days=None):
    """
    Returns a key for caching the weather information of a City

    Args:
        city (str): Name of the city
        country (str): Country code
        days (int): Number of days to get forecast
    """
    if days is None:
        return city.upper().replace(' ', '') + country.upper()
    else:
        return city.upper().replace(' ', '') + country.upper() + str(days)


def get_wind_angle_description(deg):
    """
    Returns a human-readable description of the wind's direction

    Args:
        deg (int): Angle of the wind's direction
    """
    if deg < 0:
        while deg < 0:
            deg += 360
    if deg > 360:
        while deg > 360:
            deg -= 360

    if 0 <= deg < 90:
        if deg == 0:
            return 'west'
        elif deg < 45:
            return 'west-southwest'
        elif deg == 45:
            return 'southwest'
        else:
            return 'south-southwest'
    elif 90 <= deg < 180:
        if deg == 90:
            return 'south'
        elif deg < 135:
            return 'south-southeast'
        elif deg == 135:
            return 'southeast'
        else:
            return 'east-southeast'
    elif 180 <= deg < 270:
        if deg == 180:
            return 'east'
        elif deg < 225:
            return 'east-northeast'
        elif deg == 225:
            return 'northeast'
        else:
            return 'north-northeast'
    elif 270 <= deg < 360:
        if deg == 270:
            return 'north'
        elif deg < 315:
            return 'north-northwest'
        elif deg == 315:
            return 'northwest'
        else:
            return 'west-northwest'


def get_wind_beaufort_description(wind_speed):
    """
    Returns a description of the wind based on the Beaufort scale

    Args:
        wind_speed (float): Speed of the wind in m/s

    Notes:
        More about Beaufort scale: https://en.wikipedia.org/wiki/Beaufort_scale
    """
    if wind_speed < 0.5:
        return 'Calm'
    elif wind_speed <= 1.5:
        return 'Light air'
    elif wind_speed <= 3.3:
        return 'Light breeze'
    elif wind_speed <= 5.5:
        return 'Gentle breeze'
    elif wind_speed <= 7.9:
        return 'Moderate breeze'
    elif wind_speed <= 10.7:
        return 'Fresh breeze'
    elif wind_speed <= 13.8:
        return 'Strong breeze'
    elif wind_speed <= 17.1:
        return 'Moderate Gale'
    elif wind_speed <= 24.4:
        return 'Gale'
    elif wind_speed <= 28.4:
        return 'Storm'
    elif wind_speed <= 32.6:
        return 'Violent storm'
    else:
        return 'Hurricane force'