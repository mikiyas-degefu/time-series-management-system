from django.urls import path
from .views import index , topic , delete_topic , edit_topic

urlpatterns = [
    path('', index, name='index'),
    path('topic/', topic, name='topic'),
    path('delete_topic/<int:id>', delete_topic, name='delete_topic'),
    path('edit_topic/', edit_topic, name='edit_topic'),

]