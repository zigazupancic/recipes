from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^all/', views.all_recipes, name='all_recipes'),
    url(r'^search', views.search, name='search'),
    url(r'^publish', views.publish, name='publish')
]
