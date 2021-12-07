from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, PlanForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import Seller, Product, Sale


@unauthenticated_user
def register(request):

    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='seller')
            user.groups.add(group)

            Seller.objects.create(
                user = user,
                first_name = user.username
            )

            messages.success(request, f'Account was created new user added: {username}')
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

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

@login_required(login_url='login')
@admin_only
def home(request):
    return render(request,'main.html')



'''----------------------------------------------------------SELLER MENU'''
@login_required(login_url='login')
@allowed_users(allowed_roles=['seller'])
def sellerPage(request):
    """Пока что отдадим все продажи юзера"""
    sales = request.user.seller.sale_set.all()
    context = {'sales': sales}
    return render(request, 'seller/seller_page.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'seller'])
def user_info(request):
    return render(request, 'seller/user_info.html')

@allowed_users(allowed_roles=['seller'])
def user_statistics(request):
    return render(request, 'seller/user_statistics.html')

def user_last_sales(request):
    sales = request.user.seller.sale_set.all()
    context = {'sales': sales}
    return \
        render(request, 'seller/user_last_sales.html', context)

def user_plan(request):
    return render(request, 'seller/sellers_plan.html')

'''----------------------------------------------------------'''

def all_sellers(request):
    '''Просто список отдаем всех юзеров с переходом вних'''
    print(Seller.objects.all())
    return render(request, 'admin/all_sellers.html')

def last_10_sales(request):
    sales = Sale.objects.all().order_by('date_created')[:10]
    sales = reversed(sales)
    context = {'sales':sales}
    return render(request, 'admin/last_sales.html', context)

def add_plan_to_seller(request):
    '''Надо с видоса посмотреть(создать форму и придумать model)'''
    if request.method =="POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': PlanForm()}
    return render(request, 'admin/add_plan.html', context)

def statistics(request):
    """statistics of the best sellers
    """
    return render(request, 'admin/statistics.html')
