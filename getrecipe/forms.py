from django import forms
from django.shortcuts import get_list_or_404
from .models import Sestavina

class IngredientsForm(forms.Form):
    available_ingredients = get_list_or_404(Sestavina)
    choices = []
    for ingredient in available_ingredients:
        choices.append((ingredient.id, ingredient.ime))
    ingredients = forms.MultipleChoiceField(choices=choices)
