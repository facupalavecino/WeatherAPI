from datetime import datetime
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .requests import get_forecast_data, get_weather_data
from .utils import get_cache_key


@api_view(['GET'])
def weather_view(request, format=None):
    """
    Retrieves the Weather information for a given city and country from an external API and returns it in a human-readable format. \n
    It also caches the information for 2 minutes.
    """
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

    key = get_cache_key(params['city'], params['country'])

    city_info = cache.get(key)
    if city_info is not None:
        return Response(data=dict(city_info), status=status.HTTP_200_OK)
    else:
        try:
            city = get_weather_data(params.get('city'), params.get('country'), requested_time)
            ret_val = city.get_readable()
            cache.set(key, ret_val, settings.CUSTOM_CACHE_TIMEOUT)
            return Response(data=ret_val, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=e.args[1].json(), status=e.args[1].status_code)


@api_view(['GET'])
def forecast_view(request, format=None):
    """
    Retrieves the Weather forecast for a given city and country from an external API and returns it in a human-readable format. \n
    It also caches the information for 2 minutes.
    """

    requested_time = datetime.now()
    params = {
        'city': request.query_params.get('city', None),
        'country': request.query_params.get('country', None),
        'days': request.query_params.get('days', None)
    }

    for k, v in params.items():
        if v is None:
            return Response(data=f"Required parameter '{k}' is missing", status=status.HTTP_400_BAD_REQUEST)
    if len(params['country']) != 2:
        return Response(data=f"Parameter 'country' must be a 2-characters long code", status=status.HTTP_400_BAD_REQUEST)
    try:
        params['days'] = int(params.get('days'))
        if not (0 <= params.get('days') <= 6):
            return Response(data=f"Parameter 'days' must be an int between 0 and 6", status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        return Response(data=f"Parameter 'days' must be an int between 0 and 6", status=status.HTTP_400_BAD_REQUEST)

    params['city'] = params.get('city').title()
    params['country'] = params.get('country').lower()

    key = get_cache_key(params['city'], params['country'], params['days'])

    city_info = cache.get(key)

    if city_info is not None:
        return Response(data=dict(city_info), status=status.HTTP_200_OK)
    else:
        try:
            city = get_forecast_data(params.get('city'), params.get('country'), params.get('days'), requested_time)

            ret_val = city.get_readable()
            cache.set(key, ret_val, settings.CUSTOM_CACHE_TIMEOUT)

            return Response(data=ret_val, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=e.args[1].json(), status=e.args[1].status_code)
