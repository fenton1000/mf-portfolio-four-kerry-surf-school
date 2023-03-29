from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Customer, Booking
from .forms import CustomerForm, BookingForm


def customer_account_required(func):
    """
    Decorator checks that a customer profile exists and
    redirects to profile creation if it does not exist.
    """
    def wrapper(request):
        try:
            request.user.customer
        except ObjectDoesNotExist:
            return redirect('customer_first_login')
        return func(request)
    return wrapper


def index(request):
    """
    Creates the home page.
    """
    return render(request, 'index.html')


@login_required
@customer_account_required
def customer(request):
    """
    Creates the customer's account dashboard.
    """
    return render(request, 'customer.html')


def signup_login_links(request):
    """
    Creates the sign up or log in links page.
    """
    return render(request, 'signup_login_links.html')


@login_required
def customer_first_login(request):
    """
    Creates the complete customer profile form and
    page and handles the form when submitted.
    """
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = request.user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_num = form.cleaned_data['phone_num']
            date_of_birth = form.cleaned_data['date_of_birth']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            Customer.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_num=phone_num,
                date_of_birth=date_of_birth,
                height=height,
                weight=weight,
            )
            messages.success(
                request, 'Your profile has been saved!')
            return redirect('customer')
    context = {
        'form': form
    }
    return render(request, 'customer_first_login.html', context)


@login_required
def edit_customer(request):
    """
    Creates the edit customer profile page and handles
    the change form when submitted.
    """
    customer = get_object_or_404(Customer, user=request.user)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('customer')
    context = {
        'customer': customer,
        'form': form
    }
    return render(request, 'edit_profile.html', context)


@login_required
def delete_user(request):
    """
    Deletes an authenticated logged in users account.
    """
    user = get_object_or_404(User, id=request.user.id)
    user.delete()
    messages.success(request, 'Your Customer Account has been deleted!')
    return redirect('index')


@login_required
@customer_account_required
def make_booking(request):
    """
    Creates the make a booking page and handles
    the booking form when submitted.
    """
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            customer = request.user
            ability_level = form.cleaned_data['ability_level']
            lesson_date = form.cleaned_data['lesson_date']
            lesson_time = form.cleaned_data['lesson_time']
            customer_requests = form.cleaned_data['customer_requests']
            if Booking.objects.filter(
                customer=customer,
                lesson_date=lesson_date,
                lesson_time=lesson_time,
            ).exists():
                messages.warning(request, 'This booking already exists!')
                return redirect('customer')
            Booking.objects.create(
                customer=customer,
                ability_level=ability_level,
                lesson_date=lesson_date,
                lesson_time=lesson_time,
                customer_requests=customer_requests
            )
            messages.success(
                request, 'Booking Complete! See View Your Bookings')
            return redirect('customer')
    context = {
        'form': form
    }
    return render(request, 'make_booking.html', context)


@login_required
@customer_account_required
def view_bookings(request):
    """
    Creates the view bookings page.
    """
    bookings = Booking.objects.filter(customer=request.user)
    context = {
        'bookings': bookings
    }
    return render(request, 'view_bookings.html', context)


@login_required
def edit_booking(request, booking_id):
    """
    Creates the edit a booking page and handles
    the edit booking form when submitted.
    """
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    form = BookingForm(instance=booking)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            pk = booking.id
            customer = request.user
            lesson_date = form.cleaned_data['lesson_date']
            lesson_time = form.cleaned_data['lesson_time']
            if Booking.objects.filter(
                customer=customer,
                lesson_date=lesson_date,
                lesson_time=lesson_time,
            ).exists():
                check_booking = Booking.objects.get(
                    customer=customer,
                    lesson_date=lesson_date,
                    lesson_time=lesson_time,
                )
                if pk != check_booking.id:
                    messages.warning(request, 'This booking already exists!')
                    return redirect('customer')
            form.save()
            messages.success(request, 'Your booking has been updated!')
            return redirect('view_bookings')
    context = {
        'booking': booking,
        'form': form
    }
    return render(request, 'edit_booking.html', context)


@login_required
def delete_booking(request, booking_id):
    """
    Deletes a booking.
    """
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    booking.delete()
    messages.success(request, 'Your booking has been cancelled!')
    return redirect('view_bookings')
