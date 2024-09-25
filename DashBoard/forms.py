from django import forms
from .models import Dashboard


class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }