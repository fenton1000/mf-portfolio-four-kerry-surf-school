from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
            messages.success(
                request, 'Email address and telephone number saved!')
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
            if Booking.objects.filter(
                customer=customer,
                first_name=first_name,
                last_name=last_name,
                lesson_date=lesson_date,
                lesson_time=lesson_time,
                ).exists():
                messages.warning(request, 'This booking already exists!')
                return redirect('customer')
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
            messages.success(
                request, 'Booking Complete! See View Your Bookings')
            return redirect('customer')
    form = BookingForm()
    context = {
        'form': form
    }
    return render(request, 'make_booking.html', context)


def view_bookings(request):
    bookings = Booking.objects.filter(customer=request.user)
    context = {
        'bookings': bookings
    }
    return render(request, 'view_bookings.html', context)


def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            pk = booking.id
            customer = request.user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            lesson_date = form.cleaned_data['lesson_date']
            lesson_time = form.cleaned_data['lesson_time']
            if Booking.objects.filter(
                customer=customer,
                first_name=first_name,
                last_name=last_name,
                lesson_date=lesson_date,
                lesson_time=lesson_time,
                ).exists():
                check_booking = Booking.objects.get(
                    customer=customer,
                    first_name=first_name,
                    last_name=last_name,
                    lesson_date=lesson_date,
                    lesson_time=lesson_time,
                )
                if pk != check_booking.id:
                    messages.warning(request, 'This booking already exists!')
                    return redirect('customer')
            form.save()
            messages.success(request, 'Your booking has been updated!')
            return redirect('view_bookings')
    form = BookingForm(instance=booking)
    context = {
        'booking': booking,
        'form': form
    }
    return render(request, 'edit_booking.html', context)


def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    booking.delete()
    messages.success(request, 'Your booking has been cancelled!')
    return redirect('view_bookings')
