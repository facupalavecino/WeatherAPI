from datetime import datetime
import pytz
import requests
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import WeatherInformation


@api_view(['GET'])
def weather_view(request, format=None):
    """
    Retrieves the Weather information for a given city and country from an external API and returns it in a human-readable format. \n
    It also caches the information for 2 minutes.
    """
    owm_api_key = settings.OWM_API.get('KEY')
    owm_api_url = settings.OWM_API.get('BASE_URL')
    requested_time = datetime.now()

    params = {
        'city': request.query_params.get('city', None),
        'country': request.query_params.get('country', None)
    }

    for k, v in params.items():
        if v is None:
            return Response(data=f"Required parameter '{k}' is missing", status=status.HTTP_400_BAD_REQUEST)

    if len(params['country']) != 2:
        return Response(data=f"Parameter 'country' must be a 2-characters long code", status=status.HTTP_400_BAD_REQUEST)

    params['city'] = params.get('city').title()
    params['country'] = params.get('country').lower()

    weather = cache.get(f"{params.get('city')}_{params.get('country')}")

    if weather is not None:
        return Response(data=dict(weather), status=status.HTTP_200_OK)
    else:
        req = requests.get(f"{owm_api_url}/weather", params={'q': params.get('city') + ',' + params.get('country'),
                                                             'appid': owm_api_key})
        if req.status_code == 200:
            req_data = req.json()
            req_data['requested_time'] = requested_time
            ret_val = WeatherInformation(req_data).__dict__
            cache.set(f"{params.get('city')}_{params.get('country')}", ret_val, settings.CUSTOM_CACHE_TIMEOUT)
            return Response(data=ret_val, status=req.status_code)

        return Response(data=req.json(), status=req.status_code)
