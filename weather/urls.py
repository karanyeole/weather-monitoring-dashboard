# weather/urls.py
from django.urls import path
from .views import index_view, daily_summary_view, alerts_view

urlpatterns = [
    path('', index_view, name='index'),
    path('summary/', daily_summary_view, name='summary'),
    path('alerts/', alerts_view, name='alerts'),
]
