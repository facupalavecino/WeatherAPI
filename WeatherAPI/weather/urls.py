from django.urls import path
from rest_framework import routers
from .views import weather_view


urlpatterns = [
    path('weather/', weather_view)
]
