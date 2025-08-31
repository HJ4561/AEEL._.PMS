from .models import CustomUser

def user_role_counts(request):
    return {
        'manager_count': CustomUser.objects.filter(role='manager').count(),
        'engineer_count': CustomUser.objects.filter(role='engineer').count(),
        'admin_count': CustomUser.objects.filter(role='admin').count(),
    }