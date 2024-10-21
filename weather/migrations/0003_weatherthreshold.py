# Generated by Django 5.1.2 on 2024-10-21 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_weatherthreshold'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherThreshold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('temperature_threshold', models.FloatField()),
                ('weather_condition', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]