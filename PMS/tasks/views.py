from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task, Project
from .forms import TaskForm, ProjectForm
from pms_users.models import CustomUser
import logging

logger = logging.getLogger(__name__)

@login_required
def manager_dashboard(request):
    if request.user.role != 'manager':
        logger.debug(f"User {request.user.email} attempted to access manager_dashboard but is not a manager")
        return redirect('engineer_dashboard')
    tasks = Task.objects.all()
    engineers = CustomUser.objects.filter(role='engineer')
    status_counts = {
        'todo': tasks.filter(status='todo').count(),
        'inprogress': tasks.filter(status='inprogress').count(),
        'done': tasks.filter(status='done').count(),
    }
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            logger.info(f"Task {task.title} created by {request.user.email}")
            return redirect('manager_dashboard')
        else:
            logger.error(f"Task form invalid: {form.errors}")
    context = {'tasks': tasks, 'engineers': engineers, 'form': form, 'status_counts': status_counts}
    return render(request, 'manager_dashboard.html', context)

@login_required
def engineer_dashboard(request):
    if request.user.role != 'engineer':
        logger.debug(f"User {request.user.email} attempted to access engineer_dashboard but is not an engineer")
        return redirect('manager_dashboard')
    tasks = Task.objects.filter(assigned_to=request.user)
    total_tasks = tasks.count()
    completed = tasks.filter(status='done').count()
    progress = (completed / total_tasks * 100) if total_tasks > 0 else 0
    context = {'tasks': tasks, 'progress': progress}
    return render(request, 'engineer_dashboard.html', context)

@login_required
def create_project(request):
    if request.user.role != 'manager':
        logger.debug(f"User {request.user.email} attempted to access create_project but is not a manager")
        return redirect('engineer_dashboard')
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            # Save many-to-many relationship
            project.assigned_engineers.set(form.cleaned_data['assigned_engineers'])
            logger.info(f"Project {project.title} created by {request.user.email}")
            return redirect('manager_dashboard')
        else:
            logger.error(f"Project form invalid: {form.errors}")
    context = {'form': form}
    return render(request, 'create_project.html', context)