from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm

@login_required(login_url='login')
def index(request):
    return render(request,'base.html')

def register(request):
    if request.user.is_authenticated:
        print('is already authorized')
        return redirect('home')
    else:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get['username']
                messages.success(request, 'Account was created')
                return redirect('login')
        context = {'form':form}
        return render(request, 'register.html', context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')
    context = {}

    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def sellerPage(request):
    context = {}
    return render(request, 'seller_page.html')