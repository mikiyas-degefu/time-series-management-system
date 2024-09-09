from django import forms

class ImportFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class' : 'form-control'
    }))


data_point_type = [
    ('yearly', 'Yearly'),
    ('quarterly', 'Quarterly'),
    ('monthly', 'Monthly'),
]


class ImportFileIndicatorAddValueForm(forms.Form):
    type_of_data = forms.ChoiceField(required=True, choices=data_point_type, widget=forms.Select(attrs={
        'class' : 'form-select'
    }))
    file = forms.FileField(required=True,widget=forms.ClearableFileInput(attrs={
        'class' : 'form-control'
    }))