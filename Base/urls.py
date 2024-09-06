from django.urls import path
from .api.view import(
    get_indicators,
)

urlpatterns = [
    path('indicator-lists/<str:id>', get_indicators)
]