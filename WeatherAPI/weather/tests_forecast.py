from django.test import TestCase, Client
from django.urls import reverse

client = Client()


class ForecastViewTestCase(TestCase):

    def test_validates_parameters(self):
        """ The function validates required parameters """
        response_no_days = client.get(reverse('forecast'), {'city': 'La Plata', 'country': 'ar'})
        response_7_days = client.get(reverse('forecast'), {'city': 'La Plata', 'country': 'ar', 'days': 7})

        self.assertEqual(response_no_days.status_code, 400)
        self.assertEqual(response_7_days.status_code, 400)

    def test_ends_gracefully_if_cannot_find_location(self):
        """ The function ends gracefully if the location is not found in the external API """
        external_api_err_msg = {'cod': '404', 'message': 'city not found'}
        response = client.get(reverse('forecast'), {'city': '´1p23{', 'country': 'ar', 'days': 1})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), external_api_err_msg)
