# weather/apps.py

from django.apps import AppConfig
import threading
import time

class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

    def ready(self):
        # Delay importing views to avoid AppRegistryNotReady error
        from django.conf import settings

        # Start the scheduler after Django finishes initializing
        def run_scheduler():
            from .views import fetch_and_process_weather_data  # Import here, after app is ready
            while True:
                fetch_and_process_weather_data()
                time.sleep(300)  # Sleep for 5 minutes

        if settings.DEBUG:  # Ensure it's only run once in dev mode
            thread = threading.Thread(target=run_scheduler)
            thread.daemon = True
            thread.start()
