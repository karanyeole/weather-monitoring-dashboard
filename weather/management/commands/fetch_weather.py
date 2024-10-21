# weather/management/commands/fetch_weather.py
import requests
from django.core.management.base import BaseCommand
from weather.models import DailySummary, Alert, WeatherThreshold
from django.db import transaction

class Command(BaseCommand):
    help = 'Fetch weather data from OpenWeatherMap API'

    def handle(self, *args, **options):
        cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
        api_key = '4d7f22a788c289ea011b322c26608c4b'  # Replace with your actual API key
        base_url = 'https://api.openweathermap.org/data/2.5/weather'

        with transaction.atomic():  # Use atomic transaction
            for city in cities:
                response = requests.get(f"{base_url}?q={city}&appid={api_key}&units=metric")
                data = response.json()
                if response.status_code == 200:
                    main = data['main']
                    weather = data['weather'][0]
                    temp = main['temp']
                    dominant_condition = weather['main']

                    # Store data in the database
                    DailySummary.objects.update_or_create(
                        city=city,
                        defaults={
                            'avg_temp': temp,
                            'max_temp': max(temp, main.get('temp_max', temp)),
                            'min_temp': min(temp, main.get('temp_min', temp)),
                            'dominant_weather': dominant_condition
                        }
                    )

                    # Check for alerts against the thresholds
                    thresholds = WeatherThreshold.objects.filter(city=city)
                    for threshold in thresholds:
                        if temp > threshold.temperature_threshold:
                            Alert.objects.create(
                                city=city,
                                message=f"Temperature exceeds {threshold.temperature_threshold}°C: {temp}°C"
                            )
                            print(f"Alert created for {city}: Temperature exceeds threshold.")

                else:
                    print(f"Failed to retrieve data for {city}: {data.get('message')}")
