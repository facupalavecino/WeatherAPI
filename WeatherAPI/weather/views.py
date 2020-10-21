from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.cache import cache
from datetime import datetime

@api_view(['GET'])
def weather_view(request, format=None):
    """
    Returns the Weather information for a given city and country
    """

    params = {
        'city': request.query_params.get('city', None),
        'country': request.query_params.get('country', None),
        'requested_time': str(datetime.now())
    }

    for k, v in params.items():
        if v is None:
            return Response(data=f"Required parameter '{k}' is missing", status=status.HTTP_400_BAD_REQUEST)

    if len(params['country']) != 2:
        return Response(data=f"'country' value's length must be 2", status=status.HTTP_400_BAD_REQUEST)

    params['city'] = params.get('city').title()
    params['country'] = params.get('country').lower()

    weather = cache.get(f"{params.get('city')}_{params.get('country')}")

    if weather is not None:
        print(f"Weather has been retrieved from cache: {str(weather)}")
        return Response(data=f"{weather}", status=status.HTTP_200_OK)
    else:
        # Perform get to external API
        cache.set(f"{params.get('city')}_{params.get('country')}", str(params), 60*2)
        print(f"A new value has been cached for 2 mintues: {str(params)}")
    return Response(data=f"{str(params)}", status=status.HTTP_200_OK)
