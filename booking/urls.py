from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customer/', views.customer, name='customer'),
    path('customer/firstlogin/', views.customer_first_login, name='customer_first_login'),
    path('signuporlogin/', views.signup_login_links, name='signup_login_links'),
]
