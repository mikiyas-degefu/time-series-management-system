from django.urls import path
from .api.view import *
from .views import *

from UserManagement.views import login_view , logout_view

urlpatterns = [
    path('indicator-lists/<str:id>', get_indicators),

    ###Auth
    path('login/',login_view,name="login"),
    path('logout/',logout_view,name="logout"),



    ###Api
    path('topic_list/', topic_lists),
    path('count_indicator_by_category/<str:id>/', count_indicator_by_category),
    path('filter_by_category_with_value/', filter_by_category_with_value),
    
    

    
    path('indicator-lists/<str:id>/', get_indicators),
    path('filter_topic_and_category/', filter_topic_and_category),
    path('filter_indicator_by_category/<str:id>/', filter_indicator_by_category),
   



    path('filter_indicator_by_category/<str:id>/', filter_indicator_by_category),
    path('filter_indicator_annual_value/', filter_indicator_annual_value),
    path('filter_indicator_detail_annual_value/<str:id>/', detail_indicator_with_children),
    path('indicator_graph/<str:id>/', indicator_graph),


    path('recent_data_for_topic/<str:id>', recent_data_for_topic),





    ###User
    path('', index, name='user-index'),
    path('indicator_detail_view/<str:id>/', indicator_detail_view, name='indicator_detail_view'),




]