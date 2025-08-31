from django.urls import path
from .views import manager_dashboard, engineer_dashboard, create_project

urlpatterns = [
    path('manager_dashboard/', manager_dashboard, name='manager_dashboard'),
    path('engineer_dashboard/', engineer_dashboard, name='engineer_dashboard'),
    path('create_project/', create_project, name='create_project'),
]