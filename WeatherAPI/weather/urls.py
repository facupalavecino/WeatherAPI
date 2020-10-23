from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from .views import weather_view, forecast_view


urlpatterns = [
    url('weather/', weather_view, name='weather'),
    url('forecast/', forecast_view, name='forecast')
]
