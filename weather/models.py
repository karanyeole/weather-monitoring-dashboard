# weather/models.py
from django.db import models

class DailySummary(models.Model):
    city = models.CharField(max_length=100)
    avg_temp = models.FloatField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    dominant_weather = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.timestamp}"

class Alert(models.Model):
    city = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.city} at {self.timestamp}"

class WeatherThreshold(models.Model):
    city = models.CharField(max_length=100)
    temperature_threshold = models.FloatField()
    weather_condition = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Threshold for {self.city} - Temp: {self.temperature_threshold}"
