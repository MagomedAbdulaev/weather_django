from django.test import TestCase
from django.urls import reverse

class WeatherTemplateTests(TestCase):
    def test_template_renders_weather(self):
        url = reverse('weather:home')
        weather_data = [
            {
                'temp': 20,
                'feels_like': 18,
                'windy': 5,
                'date': '17 июля 09:00',
                'weather': 'images/sun.png',
                'cloudy': 'очень низкая'
            }
        ]
        context = {
            'weather': weather_data,
            'city': 'London'
        }
        response = self.client.get(url, {'city': 'London'})
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, '17 июля 09:00')
        self.assertContains(response, 'Температура: 20°')
        self.assertContains(response, 'Ощущается как: 18°')
        self.assertContains(response, 'Скорость ветра: 5 м/с')
        self.assertContains(response, 'Облачность: очень низкая')

    def test_template_renders_error(self):
        url = reverse('weather:home')
        response = self.client.get(url, {'city': 'NonExistentCity'})
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Город не найден')
