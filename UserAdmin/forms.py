from django import forms
from Base.models import Topic

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title_ENG', 'title_AMH', 'icon', 'is_dashboard']
        widgets = {
            'title_ENG': forms.TextInput(attrs={'class': 'form-control'}),
            'title_AMH': forms.TextInput(attrs={'class': 'form-control'}),
            'is_dashboard': forms.CheckboxInput(attrs={'class': 'form-check-input ml-3'}),
        }