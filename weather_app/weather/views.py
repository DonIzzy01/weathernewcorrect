from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Post, City
from .forms import PostForm, CustomUserCreationForm

# weather/views.py
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'weather/register.html', {'form': form})  # Correct path

# weather/views.py
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('weather')  # Redirect to the weather page after login
        else:
            return render(request, 'weather/login.html', {'error': 'Invalid credentials'})
    return render(request, 'weather/login.html')  # Correct path

def user_logout(request):
    logout(request)
    return redirect('login')

def get_weather(city):
    api_key = settings.WEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

def weather_view(request):
    weather_data = []
    
    if request.method == 'POST':
        city = request.POST['city']
        city_weather = get_weather(city)
        if city_weather and city_weather.get('main'):
            weather = {
                'city': city,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }
            weather_data.append(weather)
        else:
            weather_data.append({'city': city, 'error': 'City not found'})

    cities = City.objects.all()
    for city in cities:
        city_weather = get_weather(city.name)
        if city_weather and city_weather.get('main'):
            weather = {
                'city': city.name,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }
            weather_data.append(weather)

    return render(request, 'weather/weather.html', {'weather_data': weather_data})

def post_list(request):
    posts = Post.objects.all()  # Fetch all posts from the database
    return render(request, 'weather/post_list.html', {'posts': posts})

# weather/views.py
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save to the database yet
            post.user = request.user  # Set the user to the currently logged-in user
            post.save()  # Now save the post
            return redirect('post_list')  # Redirect to the post list after creation
    else:
        form = PostForm()
    return render(request, 'weather/post_form.html', {'form': form})  # Corrected path

def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return redirect('post_list')
    return render(request, 'weather/post_form.html', {'post': post})  # Corrected path

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('post_list')

def home(request):
    return render(request, 'weather/home.html')  # Correct path