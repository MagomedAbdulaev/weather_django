from django.urls import path
from .views import *
#http://api.openweathermap.org/data/2.5/weather?appid=63ccfc4fc9a730b1a6e126c18afedb03&q=Moscow
app_name = 'weather'


urlpatterns = [
    path('', home, name='home'),
    path('cities/', cities_json,),
    path('get_cities_count/', get_count_all_cities,),
]
