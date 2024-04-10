from django import forms

from .models import Category


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Поиск', required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Поиск'})
    )
    category = forms.ModelChoiceField(
        label='Категория', required=False,
        queryset=Category.objects.all()
    )
