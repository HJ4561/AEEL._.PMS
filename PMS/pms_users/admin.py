from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_queryset(self, request):
        return super().get_queryset(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['manager_count'] = CustomUser.objects.filter(role='manager').count()
        extra_context['engineer_count'] = CustomUser.objects.filter(role='engineer').count()
        extra_context['admin_count'] = CustomUser.objects.filter(role='admin').count()
        return super().changelist_view(request, extra_context=extra_context)