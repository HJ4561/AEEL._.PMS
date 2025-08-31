from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import SignupForm, LoginForm
from .models import CustomUser
import logging

logger = logging.getLogger(__name__)

class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'  # Assumes templates/registration/signup.html
    success_url = '/dashboard/'

    def form_valid(self, form):
        logger.debug(f"Signup form submitted with data: {form.cleaned_data}")
        user = form.save()
        authenticated_user = authenticate(email=user.email, password=form.cleaned_data['password1'])
        if authenticated_user is not None:
            login(self.request, authenticated_user)
            logger.info(f"User {user.email} signed up and logged in successfully")
        else:
            logger.error(f"Authentication failed for user {user.email}")
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        logger.debug(f"Redirecting user {user.email} with role {user.role}")
        if user.role == 'manager':
            return '/manager_dashboard/'
        elif user.role == 'engineer':
            return '/engineer_dashboard/'
        return '/dashboard/'

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'  # Assumes templates/registration/login.html

    def form_valid(self, form):
        logger.debug(f"Login form submitted with email: {form.cleaned_data['username']}")
        response = super().form_valid(form)
        logger.info(f"User {self.request.user.email} logged in successfully")
        return response

    def get_success_url(self):
        user = self.request.user
        logger.debug(f"Redirecting user {user.email} with role {user.role}")
        if user.role == 'manager':
            return '/manager_dashboard/'
        elif user.role == 'engineer':
            return '/engineer_dashboard/'
        return '/dashboard/'

def dashboard(request):
    if not request.user.is_authenticated:
        logger.debug("Unauthenticated user redirected to login")
        return redirect('login')
    logger.debug(f"Authenticated user {request.user.email} with role {request.user.role}")
    if request.user.role == 'manager':
        return redirect('manager_dashboard')
    elif request.user.role == 'engineer':
        return redirect('engineer_dashboard')
    return render(request, 'base.html')