from django.shortcuts import render

# Create your views here.

def base_index(request):
    return render(request, 'Base/index.html')

def about(request):
    return render(request, 'Base/about.html')    

def contact(request):
    return render(request, 'Base/contact.html')


