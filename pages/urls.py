from django.urls import path 
from . import views


urlpatterns = [
    path (''     , views.index , name='index'),

    path('coffee',  views.coffee,  name='coffee'),
    path('about',   views.about ,  name='about'),
]
