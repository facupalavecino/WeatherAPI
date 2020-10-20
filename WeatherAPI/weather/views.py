from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['GET'])
def weather_view(request, format=None):
    """
    Returns the Weather information for a given city and country
    """

    params = {
        'city': request.query_params.get('city', None),
        'country': request.query_params.get('country', None)
    }

    for k, v in params.items():
        if v is None:
            return Response(data=f"Required parameter '{k}' is missing", status=status.HTTP_400_BAD_REQUEST)

    if len(params['country']) != 2:
        return Response(data=f"'country' value's length must be 2", status=status.HTTP_400_BAD_REQUEST)

    return Response(data=f"I'm working! Params received: {str(params)}", status=status.HTTP_200_OK)