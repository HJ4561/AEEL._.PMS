from django.urls import path
from .views import manager_dashboard, engineer_dashboard

urlpatterns = [
    path('', manager_dashboard, name='manager_dashboard'),
    path('', engineer_dashboard, name='engineer_dashboard'),
]