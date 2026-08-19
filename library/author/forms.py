from django import forms
from .models import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'surname', 'patronymic']
        labels = {
            'name': 'Name',
            'surname': 'Surname',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
        }