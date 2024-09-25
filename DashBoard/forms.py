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
        exclude = ('for_row', 'for_dashboard', 'component', 'rank')
        widgets = {
            #'indicator' : forms.Select(attrs={'class': 'form-control'}),
            'year' : forms.Select(attrs={'class': 'form-control'}),
            'data_range_start' : forms.TextInput(attrs={'class': 'form-control'}),
            'data_range_end' : forms.TextInput(attrs={'class': 'form-control'}),
            'width' : forms.Select(attrs={'class': 'form-control'}),
            
        }