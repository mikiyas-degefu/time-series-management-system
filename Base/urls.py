from django.urls import path
from .api.view import(
    get_indicators,
)
from .api.view import(
    get_indicators,
    filter_topic_and_category,
    filter_indicator_by_category,
    filter_indicator_annual_value,
    detail_indicator_with_children
)

from UserManagement.views import login_view , logout_view

urlpatterns = [
    path('indicator-lists/<str:id>', get_indicators),



    ###Auth
    path('login/',login_view,name="login"),
    path('logout/',logout_view,name="logout"),



    ###Api
    path('indicator-lists/<str:id>', get_indicators),
    path('filter_topic_and_category/', filter_topic_and_category),
    path('filter_indicator_by_category/<str:id>/', filter_indicator_by_category),
    path('filter_indicator_annual_value/', filter_indicator_annual_value),
    path('filter_indicator_detail_annual_value/<str:id>/', detail_indicator_with_children),



]