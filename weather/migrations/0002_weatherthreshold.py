from django.db import migrations

def create_weather_thresholds(apps, schema_editor):
    WeatherThreshold = apps.get_model('weather', 'WeatherThreshold')
    WeatherThreshold.objects.create(city='Delhi', temperature_threshold=35)
    WeatherThreshold.objects.create(city='Mumbai', temperature_threshold=30)
    WeatherThreshold.objects.create(city='Chennai', temperature_threshold=32)
    WeatherThreshold.objects.create(city='Bangalore', temperature_threshold=28)
    WeatherThreshold.objects.create(city='Kolkata', temperature_threshold=33)
    WeatherThreshold.objects.create(city='Hyderabad', temperature_threshold=30)

class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_weather_thresholds),
    ]
