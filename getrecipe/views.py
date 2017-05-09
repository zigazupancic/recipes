from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Recept


def index(request):
    return render(request, 'getrecipe/index.html', {'ime': "Uporabnik"})


def detail(request, recipe_id):
    recipe = get_object_or_404(Recept, pk=recipe_id)
    return render(request, 'getrecipe/detail.html', {'recept': recipe})


def all_recipes(request):
    recipes = get_list_or_404(Recept)
    return render(request, 'getrecipe/allrecipes.html', {'recepti': recipes})
