from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else :
        form = CreateUserForm()
        
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def login(request):
    return render(request, 'users/login.html')

def logout(request):
    return render(request, 'users/logout.html')


def profile(request):
    return render(request , 'users/profile.html')


def update_profile(request):
    context = {
        
    }
    return render(request, 'users/update_profile.html', context)

