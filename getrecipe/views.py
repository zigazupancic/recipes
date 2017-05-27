from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Recept, Sestavina, Priprava
from .forms import IngredientsForm
from django.db.models import Count


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
            # vsebujejo vse sestavine).
            recipes = (Priprava.objects
                       .filter(sestavina_id__in=ingredients)
                       .values('recept_id')
                       .annotate(sestavine_count=Count('sestavina_id'))
                       .filter(sestavine_count__gte=len(ingredients) - 1))
            sestavine = Sestavina.objects.filter(id__in=ingredients)
            recepti = Recept.objects.filter(id__in=[r['recept_id'] for r in recipes])
            return render(request, 'getrecipe/search_result.html', {'sestavine': sestavine, 'recepti': recepti})
    else:
        form = IngredientsForm()
    return render(request, 'getrecipe/search.html', {'form': form})
