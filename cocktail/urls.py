"""
URL configuration for cocktail project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from alcohol.views import Index, Alcohol, Jin_list, Whisky_list, Beer_list, Cognac_list, Liqueur_list, Rum_list, Sake_list, Tequila_list, Vodka_list, Wine_list, Recommend
from alcohol.views import Bbaigan_list, Result, Service, CocktailInfo, Result2, NewRecipe, Result3
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Index.as_view(), name="index"),
    path("alcohol/", Alcohol.as_view(), name="alcohol"),
    path("jin_list/", Jin_list.as_view(), name="jin_list"),
    path("whisky/", Whisky_list.as_view(), name='whisky_list'),
    path("beer/", Beer_list.as_view(), name='beer_list'),
    path("cognac/", Cognac_list.as_view(), name='cognac_list'),
    path("liqueur/", Liqueur_list.as_view(), name='liqueur_list'),
    path("rum/", Rum_list.as_view(), name='rum_list'),
    path("sake/", Sake_list.as_view(), name='sake_list'),
    path("tequila/", Tequila_list.as_view(), name='tequila_list'),
    path("vodka/", Vodka_list.as_view(), name='vodka_list'),
    path("wine/", Wine_list.as_view(), name='wine_list'),
    path("bbaigan/", Bbaigan_list.as_view(), name='bbaigan_list'),
    path('recommend/', Recommend.as_view(), name='recommend'),
    path('result/', Result.as_view(), name='result'),
    path('service/', Service.as_view(), name='service'),
    path("cocktail_info/", CocktailInfo.as_view(), name='cocktail_info'),
    path("result2/", Result2.as_view(), name='result2'),
    path("new_recipe/", NewRecipe.as_view(), name='new_recipe'),
    path("result3/", Result3.as_view(), name='result3'),
]