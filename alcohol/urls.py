from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index, name="index"),
    path("recommend", views.Recommend, name="recommend"),
    path("cocktail_info", views.CocktailInfo, name="cocktail_info")
]