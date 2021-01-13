from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from .models import City
from .forms import CityForm

import requests


def index(request):
    key = 'e72efc17939398a1e3d796f7f9eca97b'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&lang=ru&units=metric&appid=' + key

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    cities = City.objects.all()
    all_cities = []

    for city in cities:
        try:
            res = requests.get(url.format(city.name)).json()
        except res.DoesNotExist:
            return HttpResponseNotFound("<h2>Person not found</h2>")
        city_info = {
            'id': city.id,
            'city': city.name,
            'temp': res["main"]["temp"],
            'humidity': res["main"]["humidity"],
            'wind_speed': res["wind"]["speed"],
            'icon': res["weather"][0]["icon"],
            'description': res["weather"][0]["description"],
        }
        all_cities.append(city_info)

    context = {
        'all_info': all_cities,
        'form': form,
    }
    return render(request, 'weather/index.html', context)


def delete(request, id):
    try:
        city = City.objects.get(id=id)
        city.delete()
        return HttpResponseRedirect("/")
    except City.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")
