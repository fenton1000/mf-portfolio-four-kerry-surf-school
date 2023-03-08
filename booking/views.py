from django.shortcuts import render, redirect
from .models import Customer
from .forms import CustomerForm


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

