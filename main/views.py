from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import RegistrationForm, LoginForm
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib import messages
# Create your views here.

def main(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'main/main.html', context)


def login(request):
    print(request.method)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Selamat Datang {username}')
            print(user)
            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, f'username dan password tidak cocok!!')
    
    form = LoginForm()
    
    context = {
        'title': 'Login',
        'form': form,
    }
    return render(request, 'auth/login.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # Valdiasi Form User
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            
            return redirect('dashboard')
    form = RegistrationForm()
    
    context = {
        'title': 'Register',
        'form': form,
    }
    return render(request, 'auth/register.html', context)