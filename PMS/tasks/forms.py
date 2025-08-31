from django import forms
from .models import Task, Project
from pms_users.models import CustomUser

class ProjectForm(forms.ModelForm):
    assigned_engineers = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='engineer'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Project
        fields = ('title', 'description', 'start_date', 'end_date', 'assigned_engineers')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Project Description'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be earlier than start date.")
        return cleaned_data

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