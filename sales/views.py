from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.decorators import api_view

from .forms import RegisterForm, PlanForm, SaleForm, DateForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import Seller, Product, Sale, WeekPlan

from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.views import APIView

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
    return render(request, 'admin/admin_page.html')



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
    user = request.user
    seller = Seller.objects.filter(user=user)[0]
    plans = WeekPlan.objects.filter(seller=seller)
    context = {'plans':plans}
    return render(request, 'seller/sellers_plan.html', context)

def add_sale(request):
    '''Возможность создавать продажы'''
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seller_page')
    context = {'form':SaleForm}
    return render(request, 'seller/add_sale.html', context)

'''----------------------------------------------------------'''

def all_sellers(request):
    '''Просто список отдаем всех юзеров с переходом вних'''
    sellers = Seller.objects.all()
    context = {'sellers': sellers}
    return render(request, 'admin/all_sellers.html', context)

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
    context = {'form': PlanForm}
    return render(request, 'admin/add_plan.html', context)

def statistics(request):
    """Вытащить всех продацев и их продажи
    1. Пока что в форме просто принять диапазон дат и отдать график
"""
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            context = {'from_date':from_date, 'to_date':to_date}
            return render(request, 'admin/statistics.html', context)
    context = {'form': DateForm}
    return render(request, 'admin/statistics.html', context)

class ChartResultView(APIView):
    def get(self, request):
        data = {}
        users = User.objects.filter(groups__name='seller')
        for user in users:
            seller = Seller.objects.filter(user=user)[0]
            sales = Sale.objects.filter(seller=seller)
            amount = sum([sale.product.price for sale in sales])
            data[seller.first_name] = amount
        return Response()

from datetime import datetime

@api_view(['GET', 'POST'])
def result_data(request):
    print(request)
    datetimes = request.data
    print('datetimes', datetimes)
    # print('from_date', datetimes['from_date'])

    data = {}
    users = User.objects.filter(groups__name='seller')
    for user in users:
        seller = Seller.objects.filter(user=user)[0]
        sales = Sale.objects.filter(seller=seller,
                                    )
        amount = sum([sale.product.price for sale in sales])
        data[seller.first_name] = amount
    return JsonResponse(data)

def test_date_view(request):
    if request.method == "POST":
        print('post')
        form = DateForm(request.POST)
        if form.is_valid():
            print('valid')
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            print(from_date)
            print(to_date)
            context = {'from_date': from_date,
                       'to_date':to_date}
            return render(request, 'admin/statistics.html', context)
    context = {'form': DateForm}
    return render(request, 'test_time.html', context)