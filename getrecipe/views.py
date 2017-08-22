from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Recept, Sestavina, Priprava
from .forms import IngredientsForm, PublishRecipeForm, RecipesForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required


def index(request):
    all_recipes = get_list_or_404(Recept)
    #return render(request, 'getrecipe/index.html', {'ime': "Uporabnik", 'recepti': recipes})
    if request.method == 'POST':
        form = RecipesForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['ime']
            recipes = (Recept.objects.filter(ime__icontains=name))
            return render(request, 'getrecipe/search_result_recipe.html', {'recepti': recipes})
    form = RecipesForm()
    return render(request, 'getrecipe/index.html', {'form': form, 'vsi_recepti': all_recipes})


def detail(request, recipe_id):
    recipe = get_object_or_404(Recept, pk=recipe_id)
    postopek = recipe.postopek.replace('&nbsp;',' ')
    return render(request, 'getrecipe/detail.html', {'recept': recipe,
                                                     'postopek': postopek})


def all_recipes(request):
    recipes = Recept.objects.all()[:30]
    return render(request, 'getrecipe/allrecipes.html', {'recepti': recipes})

def search(request):
    if request.method == 'POST':
        form = IngredientsForm(request.POST)
        if form.is_valid():
            ingredients = form.cleaned_data['sestavine']
            print(ingredients)
            if form.cleaned_data['opcija_iskanja'] == 's_in_r':
                # Vrne ID-je receptov, ki vsebujejo vse sestavine iz `ingredients`.
                recipes = (Priprava.objects
                           .filter(sestavina_id__in=ingredients)
                           .values('recept_id')
                           .annotate(sestavine_count=Count('sestavina_id'))
                           .filter(sestavine_count=len(ingredients)))
                print(recipes)
            else:
                # Vrne ID-je receptov, katerih vse sestavine so vsebovane v `ingredients`.
                exclude_recipes = (Priprava.objects.exclude(sestavina_id__in=ingredients)
                                   .values('recept_id')
                                   .distinct())
                recipes = (Recept.objects.exclude(id__in=exclude_recipes)
                           .extra(select={'recept_id': 'id'}).values('recept_id'))
            sestavine = Sestavina.objects.filter(id__in=ingredients)
            recepti = Recept.objects.filter(id__in=[r['recept_id'] for r in recipes])
            return render(request, 'getrecipe/search_result.html', {'sestavine': sestavine, 'recepti': recepti})
    form = IngredientsForm()
    return render(request, 'getrecipe/search.html', {'form': form})

#def search_result_recipe(request):
#    print("views search_recipe")
#    if request.method == 'POST':
#        form = RecipesForm(request.POST)
#        if form.is_valid():
#            name = form.cleaned_data['ime']
            #recipes = (Recept.objects
                        #.filter(ime__in=name))
#            recipes = []
#            print(recipes)
#            print("views search_recipe v IF")
#            return render(request, 'getrecipe/search_result_recipe.html', {'recepti': recipes})
#    form = RecipesForm()
#    return render(request, 'getrecipe/index.html', {'form': form})

@login_required()
def publish(request):
    if request.method == 'POST':
        form = PublishRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recept = Recept(ime=data["ime"], ocena=data["ocena"], povezava=data["povezava"],
                            povezava_do_slike_jedi=data["povezava_do_slike_jedi"], zahtevnost=data["zahtevnost"],
                            cas_priprave=data["cas_priprave"], postopek=data["postopek"])
            recept.save()
            from django.shortcuts import HttpResponse
            return HttpResponse("PUBLISHED RECIPE")
    form = PublishRecipeForm()
    return render(request, 'getrecipe/publish.html', {'form': form})
