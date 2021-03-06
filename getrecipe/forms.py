from django import forms
#from chosen import forms as chosenforms
from .models import Sestavina, TipJedi, Recept
from django.core import validators



class IngredientsForm(forms.Form):
    available_ingredients = Sestavina.objects.all()
    choices = []
    for ingredient in available_ingredients:
        choices.append((ingredient.id, ingredient.ime))
    #sestavine = forms.ChosenMultipleChoiceField(choices=choices)
    sestavine = forms.MultipleChoiceField(choices=choices)
    opcija_iskanja = forms.ChoiceField(choices=[('s_in_r', 'Recept naj vsebuje vse iskane sestavine'),
                                             ('r_in_s', 'Sestavine recepta naj bodo vsebovane v iskanih sestavinah')])


class RecipesForm(forms.Form):
    ime = forms.CharField(max_length=100, required=True)

class PublishRecipeForm(forms.Form):
    available_ingredients = Sestavina.objects.all()
    ingredients_choices = []
    for ingredient in available_ingredients:
        ingredients_choices.append((ingredient.id, ingredient.ime))
    types_of_food = TipJedi.objects.all()
    types_of_food_choices = []
    for type in types_of_food:
        types_of_food_choices.append((type.id, type.ime))

    ime = forms.CharField(max_length=200, required=True)
    ocena = forms.FloatField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(10)])
    povezava = forms.URLField(max_length=200)
    povezava_do_slike_jedi = forms.URLField(max_length=200)
    zahtevnost = forms.FloatField(validators=[validators.MinValueValidator(0), validators.MaxValueValidator(10)])
    cas_priprave = forms.FloatField(validators=[validators.MinValueValidator(0)])
    postopek = forms.CharField(max_length=10000, required=True, widget=forms.Textarea)
    tipi = forms.MultipleChoiceField(choices=types_of_food_choices, required=True)
    sestavine = forms.MultipleChoiceField(choices=ingredients_choices, required=True)
