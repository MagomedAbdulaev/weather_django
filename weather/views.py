import json
import datetime
import os
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.sessions.models import Session
from weather_django.settings import BASE_DIR
from .config import open_weather_token


def home(request):
    weather_city_five_days = []
    city = ''
    if 'recently_cities' not in request.session:
        request.session['recently_cities'] = {}

    if request.GET.get('city', False):
        city = request.GET.get('city')
        weather = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?appid={open_weather_token}&q={city}&units=metric&lang=ru',
            headers={
                'Content-Type': 'application/json',
                'accept': 'application/json',
            }
        )
        weather_data = weather.json()

        if weather_data['cod'] == '404':
            return render(request, 'home.html', {'error': 'Город не найден'})
        if weather_data['cod'] == '400':
            return render(request, 'home.html', {'error': 'Какой-то странный запрос...'})

        if city not in request.session['recently_cities']:
            # именно здесь добавляем название и количество после проверки на ошибку
            request.session['recently_cities'][city] = {'name': city, 'count': 0}

        request.session['recently_cities'][city]['count'] += 1

        request.session.modified = True

        months = {
            1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая",
            6: "июня", 7: "июля", 8: "августа", 9: "сентября", 10: "октября",
            11: "ноября", 12: "декабря"
        }

        cloudiness_description = {
            range(0, 10): 'Минимальная', range(10, 30): 'Низкая',
            range(30, 60): 'Средняя', range(60, 90): 'Высокая', range(90, 101): 'Очень высокая'
        }

        def translate_cloudiness(cloudiness):
            for cloud_range, description in cloudiness_description.items():
                if cloudiness in cloud_range:
                    return description
            return 'неизвестно'

        valid_hours = {9, 15, 21}
        weather_city_five_days = [
            {
                'temp': day['main']['temp'],
                'feels_like': day['main']['feels_like'],
                'windy': day['wind']['speed'],
                'date': f"{date_object.day} {months[date_object.month]} {date_object.hour}:00",
                'weather': day['weather'][0]['description'],
                'cloudy': translate_cloudiness(day['clouds']['all']),
                'icon': day['weather'][0]['icon'],
                'icon_url': f"http://openweathermap.org/img/w/{day['weather'][0]['icon']}.png"
            }
            for day in weather_data['list']
            if (date_object := datetime.datetime.strptime(day['dt_txt'], "%Y-%m-%d %H:%M:%S")).hour in valid_hours
        ]


    context = {
        'weather': weather_city_five_days,
        'city': city,
        'recently_cities': request.session['recently_cities'],
    }

    return render(request, 'home.html', context)


def cities_json(request):

    cities = open(os.path.join(BASE_DIR, 'weather/cities.json'))  # файл с городами
    data = json.load(cities)
    return JsonResponse(data)


def get_count_all_cities(request):

    city_count = {}
    for sess in Session.objects.all():
        for city in sess.get_decoded()['recently_cities'].values():  # перебираю все сессию и складываю количество городов
            if city['name'] in city_count:
                city_count[city['name']]['count'] += city['count']
                continue
            city_count[city['name']] = city

    context = {
        'cities': city_count
    }

    return render(request, 'cities.html', context) # JsonResponse(data) можно было использовать, но для удобства и читаемости обычный render

