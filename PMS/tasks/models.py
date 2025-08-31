from django.db import models
from pms_users.models import CustomUser

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_projects', limit_choices_to={'role': 'manager'})
    assigned_engineers = models.ManyToManyField(CustomUser, related_name='assigned_projects', limit_choices_to={'role': 'engineer'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),
        ('done', 'Done'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tasks', limit_choices_to={'role': 'engineer'})
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tasks', limit_choices_to={'role': 'manager'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
