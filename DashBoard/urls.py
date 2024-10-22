from django.urls import path
from . import views
from .api import views as api

urlpatterns = [
    path('', views.index, name='dashboard_index'),


    ###Api
    path('components/<str:id>', api.components),
]