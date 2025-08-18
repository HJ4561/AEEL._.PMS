from django import forms
from .models import Task
from pms_users.models import CustomUser

class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role='engineer'), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Task
        fields = ('title', 'description', 'assigned_to', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }