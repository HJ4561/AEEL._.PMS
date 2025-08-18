from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import SignupForm, LoginForm
from .models import CustomUser
from tasks.models import Task  # Corrected import

class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = '/dashboard/'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return response

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == 'manager':
            return '/manager_dashboard/'
        elif user.role == 'engineer':
            return '/engineer_dashboard/'
        return '/dashboard/'

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.role == 'manager':
        return redirect('manager_dashboard')
    elif request.user.role == 'engineer':
        return redirect('engineer_dashboard')
    return render(request, 'base.html')