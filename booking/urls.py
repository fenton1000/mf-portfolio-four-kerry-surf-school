from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customer/', views.customer, name='customer'),
    path(
        'customer/firstlogin/',
        views.customer_first_login,
        name='customer_first_login'
        ),
    path(
        'signuporlogin/', views.signup_login_links, name='signup_login_links'),
    path('book/', views.make_booking, name='make_booking'),
    path('mybookings/', views.view_bookings, name='view_bookings'),
    path('edit/<booking_id>', views.edit_booking, name='edit_booking'),
    path('delete/<booking_id>', views.delete_booking, name='delete_booking'),
]
