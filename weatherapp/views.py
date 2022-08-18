from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
import requests
from .forms import CityForm, CreateUserForm
from .models import City, User, Log
from django.http import JsonResponse
from datetime import datetime


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                messages.success(request, 'Account was created for ' + username)

                return redirect('login')

        context = {'form': form}
        return render(request, 'partials/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'partials/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'partials/home.html')


def location(request):
    cities = City.objects.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a0c79090e21b7d4279ef1fbc332af99b'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        print(city_weather)

        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'humidity': city_weather['main']['humidity'],
            'pressure': city_weather['main']['pressure'],
            'country': city_weather['sys']['country'],
            'sunrise': city_weather['sys']['sunrise'],
            'sunset': city_weather['sys']['sunset'],
            'windspeed': city_weather['wind']['speed']
        }

        weather_data.append(weather)


    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'partials/edit-location.html', context)


def weather(request):
    cities = City.objects.all()
    context = {
        'cities': cities
    }

    return render(request, 'partials/weather.html', context)


def weather_link(request):
    city = request.POST.get("city")

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a0c79090e21b7d4279ef1fbc332af99b'

    start = datetime.now()
    current_user = request.user
    current_time = datetime.now()
    ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
    city_weather = requests.get(url.format(city)).json()
    end = datetime.now()
    delta = end - start
    run_time = int(delta.total_seconds() * 1000)
    print(ip, current_time, current_user.id, city)

    api_status = 1
    if city_weather["cod"] == "404":
        api_status = 0
        weather = {"status": 0, "message": "City not found"}
    else:
        weather = {
            "status": 1,
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'humidity': city_weather['main']['humidity'],
            'pressure': city_weather['main']['pressure'],
            'country': city_weather['sys']['country'],
            'sunrise': city_weather['sys']['sunrise'],
            'sunset': city_weather['sys']['sunset'],
            'windspeed': city_weather['wind']['speed']
        }

    add_log = Log(ip=ip, current_time=current_time, current_user=current_user, city=city, time=run_time,
                  status=api_status)
    add_log.save()
    return JsonResponse({"response": weather})


def information(request):
    log = Log.objects.all().order_by('-current_time').values()
    print(log)

    return render(request, 'partials/information.html',
                  {'log': log})


def edit_user(request, id):
    user = get_object_or_404(User, pk=id)
    form = CreateUserForm(request.POST or None, instance=user)
    if request.POST and form.is_valid():
        form.save()

    return render(request, "partials/edit-user.html", {
        'form': form
    })


def list_user(request):
    user = User.objects.all()
    context = {'members': user}

    return render(request, 'partials/list-user.html', context)


def add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        member = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        member.save()
        return redirect('list-user')

    return render(request, 'add-user')


def delete_user(request, id):
    member = User.objects.get(id=id)
    if member.is_superuser == False:
        member.delete()
    return redirect('list-user')
