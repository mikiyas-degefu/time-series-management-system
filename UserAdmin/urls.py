from django.urls import path
from .views import index , topic

urlpatterns = [
    path('', index, name='index'),
    path('topic/', topic, name='topic'),
]