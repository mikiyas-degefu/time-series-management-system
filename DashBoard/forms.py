from django import forms
from .models import Dashboard, DashboardIndicator


class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }


class DashboardIndicatorForm(forms.ModelForm):
    class Meta:
        model = DashboardIndicator
        fields = '__all__'