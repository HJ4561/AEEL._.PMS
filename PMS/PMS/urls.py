from django.contrib import admin
from django.urls import path
from pms_users.views import SignupView, CustomLoginView, dashboard
from tasks.views import manager_dashboard, engineer_dashboard
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', dashboard, name='home'),
    path('manager_dashboard/', manager_dashboard, name='manager_dashboard'),
    path('engineer_dashboard/', engineer_dashboard, name='engineer_dashboard'),
]