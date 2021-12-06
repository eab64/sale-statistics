from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('seller_page/', views.sellerPage, name='seller_page'),

    path('home/', views.index, name = 'home')
]