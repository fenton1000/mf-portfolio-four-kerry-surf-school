from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def customer(request):
    return render(request, 'customer.html')
