from django.shortcuts import render, redirect
from .models import Customer, Booking
from .forms import CustomerForm, BookingForm


def index(request):
    return render(request, 'index.html')


def customer(request):
    return render(request, 'customer.html')


def signup_login_links(request):
    return render(request, 'signup_login_links.html')


def customer_first_login(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = request.user
            email = form.cleaned_data['email']
            phone_num = form.cleaned_data['phone_num']
            Customer.objects.create(
                user=user, email=email, phone_num=phone_num)
            return redirect('customer')
    form = CustomerForm()
    context = {
        'form': form
    }
    return render(request, 'customer_first_login.html', context)


def make_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            customer = request.user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_of_birth = form.cleaned_data['date_of_birth']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            ability_level = form.cleaned_data['ability_level']
            lesson_date = form.cleaned_data['lesson_date']
            lesson_time = form.cleaned_data['lesson_time']
            Booking.objects.create(
                customer=customer,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                height=height,
                weight=weight,
                ability_level=ability_level,
                lesson_date=lesson_date,
                lesson_time=lesson_time,
                )
            return redirect('customer')
    form = BookingForm()
    context = {
        'form': form
    }
    return render(request, 'make_booking.html', context)
