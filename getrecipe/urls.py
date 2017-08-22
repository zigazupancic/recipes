from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^all$', views.all_recipes, name='all_recipes'),
    url(r'^all/page/(?P<page_id>\d+)', views.all_recipes_page, name='all_recipes_page'),
    url(r'^search', views.search, name='search'),
    url(r'^publish', views.publish, name='publish'),
    #url(r'^recipe_search', views.search_result_recipe, name='search_result_recipe')
]
