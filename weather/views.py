# weather/views.py
import requests
from django.shortcuts import render
from .models import DailySummary, Alert
import time
import logging
from datetime import datetime
from django.core.mail import send_mail
from .models import DailySummary, Alert, WeatherThreshold

API_KEY = '4d7f22a788c289ea011b322c26608c4b'  # Replace with your OpenWeatherMap API Key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
logger = logging.getLogger(__name__)

def index_view(request):
    weather_data = []
    for city in CITIES:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
        data = response.json()
        weather_data.append({
            'name': city,
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'main': data['weather'][0]['main'],
            'timestamp': data['dt']
        })
    
    return render(request, 'index.html', {'weather_data': weather_data})

def daily_summary_view(request):
    summaries = DailySummary.objects.all()
    city_names = [summary.city for summary in summaries]
    avg_temps = [summary.avg_temp for summary in summaries]
    max_temps = [summary.max_temp for summary in summaries]
    min_temps = [summary.min_temp for summary in summaries]

    # Create the context with zipped data
    context = {
        'city_weather_data': zip(city_names, avg_temps, max_temps, min_temps)
    }

    return render(request, 'summary.html', context)



def alerts_view(request):
    # Fetch weather alerts
    alerts = Alert.objects.all()

    # Fetch daily weather summary
    daily_summary = DailySummary.objects.all()  # Use DailySummary model instead of WeatherData

    logger.debug(f'Alerts: {alerts}')
    logger.debug(f'Daily Summary: {daily_summary}')

    context = {
        'alerts': alerts,
        'daily_summaries': daily_summary,  # Ensure you pass the correct variable name
    }
    
    return render(request, 'weather/alerts.html', context)  # Adjust template path
# Rollup data and check for alerts
def fetch_and_process_weather_data():
    for city in CITIES:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
        data = response.json()
        temp = data['main']['temp']
        weather_condition = data['weather'][0]['main']
        
        # Rollup and aggregate logic
        daily_summary, created = DailySummary.objects.get_or_create(
            city=city,
            timestamp__date=datetime.now().date(),
            defaults={
                'avg_temp': temp,
                'max_temp': temp,
                'min_temp': temp,
                'dominant_weather': weather_condition
            }
        )
        
        if not created:
            daily_summary.avg_temp = (daily_summary.avg_temp + temp) / 2
            daily_summary.max_temp = max(daily_summary.max_temp, temp)
            daily_summary.min_temp = min(daily_summary.min_temp, temp)
            daily_summary.dominant_weather = weather_condition
            daily_summary.save()

        # Check for alert thresholds
        thresholds = WeatherThreshold.objects.filter(city=city)
        for threshold in thresholds:
            if temp > threshold.temperature_threshold:
                alert_message = f"Alert: {city} temperature has exceeded {threshold.temperature_threshold}°C!"
                Alert.objects.create(city=city, message=alert_message)
                send_email_alert(city, alert_message)

# Function to send email notifications for alerts (if implemented)
def send_email_alert(city, message):
    send_mail(
        subject=f"Weather Alert for {city}",
        message=message,
        from_email='weather_alerts@example.com',
        recipient_list=['user@example.com'],
        fail_silently=False,
    )


    # weather/views.py

def weather_summary_view(request):
    daily_summaries = DailySummary.objects.all()
    alerts = Alert.objects.all()
    return render(request, 'weather/alerts.html', {
        'daily_summaries': daily_summaries,
        'alerts': alerts
    })
