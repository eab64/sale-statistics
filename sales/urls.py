from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('seller_page/', views.sellerPage, name='seller_page'),
    path('user_info/', views.user_info, name = 'user_info'),
    path('user_statistics/', views.user_statistics, name='user_statistics'),
    path('user_last_sales/', views.user_last_sales, name='user_last_sales'),
    path('user_plan/', views.user_plan, name='user_plan'),

    path('all_sellers/', views.all_sellers, name='all_sellers'),
    path('last_10_sales/', views.last_10_sales, name='last_10_sales'),
    path('add_plan_to_seller/', views.add_plan_to_seller, name='add_plan_to_seller'),
    path('statistics/', views.statistics, name='statistics'),

    path('home/', views.home, name = 'home')
]