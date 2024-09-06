from django import forms
from Base.models import(
    Topic,
    Category,
    Indicator,
)

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title_ENG', 'title_AMH', 'icon', 'is_dashboard']
        widgets = {
            'title_ENG': forms.TextInput(attrs={'class': 'form-control'}),
            'title_AMH': forms.TextInput(attrs={'class': 'form-control'}),
            'is_dashboard': forms.CheckboxInput(attrs={'class': 'form-check-input ml-3'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name_ENG', 'name_AMH', 'topic', 'is_dashboard_visible']
        widgets = {
            'name_ENG': forms.TextInput(attrs={'class': 'form-control'}),
            'name_AMH': forms.TextInput(attrs={'class': 'form-control'}),
            'topic': forms.Select(attrs={'class': 'form-select'}),
            'is_dashboard_visible': forms.CheckboxInput(attrs={'class': 'form-check-input ml-3'}),
        }

class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = ['title_ENG', 'title_AMH', 'for_category', 'is_public','measurement_units', 'kpi_characteristics', 'is_dashboard_visible']
        widgets = {
            'title_ENG': forms.TextInput(attrs={'class': 'form-control'}),
            'title_AMH': forms.TextInput(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input ml-3'}),
            'measurement_units': forms.TextInput(attrs={'class': 'form-control'}),
            'kpi_characteristics': forms.Select(attrs={'class': 'form-select'}),
            'is_dashboard_visible': forms.CheckboxInput(attrs={'class': 'form-check-input ml-3'}),
        }