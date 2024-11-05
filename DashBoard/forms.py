from django import forms
from .models import Dashboard, DashboardIndicator, Row


class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }

class RowStyleForm(forms.ModelForm):
    class Meta:
        model = Row
        fields = ('style',)
        widgets = {
            'style' : forms.Select(attrs={'class' : 'form-control'})
        } 


class DashboardIndicatorForm(forms.ModelForm):
    class Meta:
        model = DashboardIndicator
        exclude = ('for_row', 'for_dashboard', 'component')
        widgets = {
            'indicator' : forms.Select(attrs={'class': 'form-control', 'multiple' : 'true'}),
            'title' : forms.TextInput(attrs={'class' : 'form-control'}),
            'description' : forms.Textarea(attrs={'class' : 'form-control'}),
            'year' : forms.Select(attrs={'class': 'form-control'}),
            'data_range_start' : forms.Select(attrs={'class': 'form-control'}),
            'data_range_end' : forms.Select(attrs={'class': 'form-control'}),
            'width' : forms.Select(attrs={'class': 'form-control'}),
            'rank' : forms.NumberInput(attrs={'class' : 'form-control'})        
        }