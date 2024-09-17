from django.shortcuts import render
from .forms import Login_Form
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages 

# Create your views here.




def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = Login_Form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request,email=email,password=password)

            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('user-index')
            elif user is not None and user.is_staff:
                login(request, user)
                return redirect('base_index')
            else:
                messages.error(request, 'Invalid Password or Email')
            form = Login_Form()
    else:
        form = Login_Form()
    return render(request, 'base/login.html', {'form': form})
