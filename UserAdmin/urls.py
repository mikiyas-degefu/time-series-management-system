from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('topic/', topic, name='topic'),
    path('delete_topic/<int:id>', delete_topic, name='delete_topic'),
    path('edit_topic/', edit_topic, name='edit_topic'),

    #Category
    path('categories/', categories, name='categories'),
    path('category/<str:id>', category, name='category'),

]