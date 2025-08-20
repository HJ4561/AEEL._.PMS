from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = None  # Remove username, use email instead
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('engineer', 'Engineer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='engineer') 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Add required fields

    def __str__(self):
        return self.email