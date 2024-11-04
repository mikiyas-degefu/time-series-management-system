from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):   
    context = {
        'dashboard' : Dashboard.objects.all().first(),
        'rows' : Row.objects.all()
    } 
    return render(request, 'dashboard/index.html' , context)
