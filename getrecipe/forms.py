from django import forms
from .models import Sestavina


class IngredientsForm(forms.Form):
    available_ingredients = Sestavina.objects.all()
    choices = []
    for ingredient in available_ingredients:
        choices.append((ingredient.id, ingredient.ime))
    ingredients = forms.MultipleChoiceField(choices=choices)
    search_type = forms.ChoiceField(choices=[('s_in_r', 'Recept naj vsebuje vse iskane sestavine'),
                                             ('r_in_s', 'Sestavine recepta naj bodo vsebovane v iskanih sestavinah')])
