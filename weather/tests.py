from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class WeatherViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('weather:home')

    @patch('requests.get')
    def test_city_found(self, mock_get):
        mock_response = {
            'cod': '200',
            'list': [
                {
                    'main': {'temp': 20, 'feels_like': 18},
                    'wind': {'speed': 5},
                    'dt_txt': '2024-07-17 09:00:00',
                    'weather': [{'description': 'clear sky'}],
                    'clouds': {'all': 0}
                },
                {
                    'main': {'temp': 22, 'feels_like': 20},
                    'wind': {'speed': 4},
                    'dt_txt': '2024-07-18 15:00:00',
                    'weather': [{'description': 'few clouds'}],
                    'clouds': {'all': 20}
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = self.client.get(self.url, {'city': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('weather', response.context)
        self.assertIn('city', response.context)
        self.assertEqual(response.context['city'], 'London')
        self.assertGreater(len(response.context['weather']), 0)

    @patch('requests.get')
    def test_city_not_found(self, mock_get):
        mock_response = {'cod': '404', 'message': 'city not found'}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = self.client.get(self.url, {'city': 'NonExistentCity'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Город не найден')

    def test_no_city_provided(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('weather', response.context)
        self.assertEqual(response.context['weather'], [])
        self.assertIn('city', response.context)
        self.assertEqual(response.context['city'], '')
