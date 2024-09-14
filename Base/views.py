from django.shortcuts import render
from .models import (
    Topic,
    Category
)


def index(request):
    return render(request, 'base/index.html')