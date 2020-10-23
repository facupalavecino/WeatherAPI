from django.test import TestCase, Client
from django.urls import reverse

client = Client()


class WeatherViewTestCase(TestCase):

    def test_validates_parameters(self):
        """ The function validates required parameters """
        response_no_city = client.get(reverse('weather'), {'country': 'ar'})
        response_no_country = client.get(reverse('weather'), {'city': 'La Plata'})
        response_long_country = client.get(reverse('weather'), {'city': 'La Plata', 'country': '123'})

        self.assertEqual(response_no_city.status_code, 400)
        self.assertEqual(response_no_country.status_code, 400)
        self.assertEqual(response_long_country.status_code, 400)

    def test_ends_gracefully_if_cannot_find_location(self):
        """ The function ends gracefully if the location is not found in the external API """
        external_api_err_msg = {'cod': '404', 'message': 'city not found'}
        response = client.get(reverse('weather'), {'city': '´1p23{', 'country': 'ar'})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), external_api_err_msg)
