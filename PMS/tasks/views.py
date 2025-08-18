from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from pms_users.models import CustomUser

@login_required
def manager_dashboard(request):
    if request.user.role != 'manager':
        return redirect('engineer_dashboard')  # Or error page
    tasks = Task.objects.all()
    engineers = CustomUser.objects.filter(role='engineer')
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('manager_dashboard')
    context = {'tasks': tasks, 'engineers': engineers, 'form': form}
    return render(request, 'tasks/manager_dashboard.html', context)

@login_required
def engineer_dashboard(request):
    if request.user.role != 'engineer':
        return redirect('manager_dashboard')  # Or error page
    tasks = Task.objects.filter(assigned_to=request.user)
    context = {'tasks': tasks}
    return render(request, 'tasks/engineer_dashboard.html', context)
@login_required
def manager_dashboard(request):
    if request.user.role != 'manager':
        return redirect('engineer_dashboard')
    tasks = Task.objects.all()
    engineers = CustomUser.objects.filter(role='engineer')
    # Add stats for chart
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
            return redirect('manager_dashboard')
    context = {'tasks': tasks, 'engineers': engineers, 'form': form, 'status_counts': status_counts}
    return render(request, 'tasks/manager_dashboard.html', context)

@login_required
def engineer_dashboard(request):
    if request.user.role != 'engineer':
        return redirect('manager_dashboard')
    tasks = Task.objects.filter(assigned_to=request.user)
    # Add progress stats
    total_tasks = tasks.count()
    completed = tasks.filter(status='done').count()
    progress = (completed / total_tasks * 100) if total_tasks > 0 else 0
    context = {'tasks': tasks, 'progress': progress}
    return render(request, 'tasks/engineer_dashboard.html', context)