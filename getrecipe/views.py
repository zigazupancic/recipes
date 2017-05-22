from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Recept, Sestavina, Priprava
from .forms import IngredientsForm


def index(request):
    return render(request, 'getrecipe/index.html', {'ime': "Uporabnik"})


def detail(request, recipe_id):
    recipe = get_object_or_404(Recept, pk=recipe_id)
    return render(request, 'getrecipe/detail.html', {'recept': recipe})


def all_recipes(request):
    recipes = get_list_or_404(Recept)
    return render(request, 'getrecipe/allrecipes.html', {'recepti': recipes})


def search(request):
    if request.method == 'POST':
        form = IngredientsForm(request.POST)
        if form.is_valid():
            ingredients = form.cleaned_data['ingredients']
            # Vrne ID-je receptov, ki vsebujejo vse sestavine iz `ingredients` ali eno manj (najprej vrne tiste ki
            # vsebujejo vse sestavine.
            recipes = Priprava.objects.raw("""
                SELECT recept_id AS id, COUNT(sestavina_id)
                FROM getrecipe_priprava
                WHERE sestavina_id IN %s
                GROUP BY recept_id
                HAVING COUNT(sestavina_id) >= %s - 1
                ORDER BY COUNT(sestavina_id) DESC;""", params=[tuple(ingredients), len(ingredients)])
            sestavine = Sestavina.objects.filter(id__in=ingredients)
            recepti = Recept.objects.filter(id__in=[r.id for r in recipes])
            return render(request, 'getrecipe/search_result.html', {'sestavine': sestavine, 'recepti': recepti})
    else:
        form = IngredientsForm()
    return render(request, 'getrecipe/search.html', {'form': form})
