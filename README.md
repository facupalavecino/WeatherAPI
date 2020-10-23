# WeatherAPI
Small API implemented with Django and Django Rest Framework that fetches weather information for cities from an external API (Open Weather Map)

## Set up
*NOTE: It is recommended to work on a Virtual Environment before setting up the project. Please refer to [the official documentation](https://docs.python.org/3/library/venv.html) to learn about Virtual Envs in Python*

1. Clone this repository to a local working folder
2. Install the requirements with `pip install -r requirements.txt`
3. Navigate to ./WeatherAPI
4. Add your Open Weather Map API KEY in `./WeatherAPI/settings.py`
4. Run the migrations `python manage.py migrate`
5. Run the project `python manage.py runserver`
6. Proceed to the Examples section to start using the API

## Testing
*NOTE: Add your Open Weather Map API Key before running tests*
Navigate to ./WeatherAPI and execute `python manage.py test`

## Examples
*NOTE: Add your Open Weather Map API Key before performing a request*

This API exposes 2 endpoints:

##### /api/weather
This endpoint fetches the current weather information for a city. Query parameters:
- city: Name of the city
    - `Buenos Aires` `New York`
- country: 2-characters long country code
    - `ar` `us`
    
##### /api/forecast
In addition to the current weather data, this endpoint includes forecast information for the next `n` days. Query parameters:
- city: Name of the city
    - `Buenos Aires` `New York`
- country: 2-characters long country code
    - `ar` `us`
- days: number of days to forecast from 0 to 6
    - `0`: no forecast
    - `6`: next 6 days
