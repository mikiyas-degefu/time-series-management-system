from django.urls import path
from .views import *

urlpatterns = [
    path('<int:id>', index, name='index'),
    path('topic/', topic, name='topic'),
    path('delete_topic/<int:id>', delete_topic, name='delete_topic'),
    path('edit_topic/', edit_topic, name='edit_topic'),


    ##Data view 
    path('data_view/', data_view, name='data_view'), 
    path('data_view_indicator_detail/<str:id>/', data_view_indicator_detail, name='data_view_indicator_detail'),
    path('data_view_indicator_update/<str:id>/', data_view_indicator_update, name='data_view_indicator_update'),

    #Category
    path('categories/', categories, name='categories'),
    path('edit_category/', update_category, name='update_category'),
    path('delete_category/<str:id>', delete_category, name='delete_category'),

    #Indicator
    path('indicators/<str:id>', indicators, name='indicators'),
    path('indicator_details/<str:id>', indicator_details, name='indicators_detail'),
    path('indicator_delete/<str:id>', delete_indicator, name='delete_indicator'),


    #Users
    path('users/', users, name='users'),
    path('user_activate/<str:id>', user_activate, name='user_activate'),



    #Years
    path('years/', years, name='years'),


    #all_indicators
    path('all_indicators/', all_indicators, name='all_indicators'),



    ##Dashboard
    path('admin_dashboard_index/', dashboard_index, name='admin-dashboard-index'),

    ##Export data
    path('export_topic/', export_topic, name='export_topic'),
    path('export_category/', export_category, name='export_category'),
    path('export_indicator/', export_indicator, name='export_indicator'),


]