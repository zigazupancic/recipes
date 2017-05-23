from django import forms
from .models import Sestavina


class IngredientsForm(forms.Form):
    available_ingredients = Sestavina.objects.all()
    choices = []
    for ingredient in available_ingredients:
        choices.append((ingredient.id, ingredient.ime))
    ingredients = forms.MultipleChoiceField(choices=choices)
