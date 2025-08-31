from django.contrib import admin
from django.urls import path, include
from pms_users.views import SignupView, CustomLoginView, dashboard
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', include('tasks.urls')),  # Include tasks URLs
]