from django.urls import path
from . import views
from .api import views as api

urlpatterns = [
    path('', views.index, name='dashboard_index'),


    ###Api
    path('components/', api.components),
    path('single_indicator_data/<str:id>/<str:year>/', api.single_indicator_data),
]