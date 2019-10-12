from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from myapp import stock_api
from myapp.forms import  UpdateProfile
from myapp.models import Stock
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
import sqlite3
from django.urls import reverse






# View for the home page - a list of 20 of the most active stocks
def index(request):
    # Query the stock table, filter for top ranked stocks and order by their rank.
    data = Stock.objects.filter(top_rank__isnull=False).order_by('top_rank')
    return render(request, 'index.html', {'page_title': 'Main', 'data': data })


# View for the single stock page
# symbol is the requested stock's symbol ('AAPL' for Apple)
def single_stock(request, symbol):

    data = stock_api.get_stock_info(symbol)
    all_companies = stock_api.get_currency()
    #check for currency type and add it to data
    for object in all_companies:
        if object['symbol'] == symbol:
            currency = object['currency']
            break

    data['currency'] = currency

    return render(request, 'single_stock.html', {'page_title': 'Stock Page - %s' % symbol, 'data': data})

@login_required
def profile(request):
    return render(request, 'profile.html')


def register(request):
    # If post -> register the user and redirect to main page
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')

        job = request.POST.get('job')

        password = request.POST.get('password')

        newuser = User.objects.create_user(username=username, email=email, password=password)
        newuser.first_name = firstname
        newuser.last_name = lastname
        # not working !!
        newuser.job = job

        newuser.save()
        return redirect('index')
    else:
        # If not post (regular request) -> render register page
        return render(request, 'register.html', {'page_title': 'Register'})

def edit_profile(request):
    args = {}

    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        # the instance=request.user : gets the user saved info
        form = UpdateProfile(instance=request.user)

        args = {'form': form}
        return render(request, 'edit_profile.html', args)

# def edit_profile(request):
#     if request.method == 'POST':
#
#         form = UpdateProfile(request.POST, instance=request.user)
#         form.actual_user = request.user
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = EditProfileForm(instance=request.user)
#         args = {'form': form}
#         return render(request, 'edit_profile.html', args)

def logout_view(request):
    logout(request)
    return redirect('index')


# API for a stock's price over time
# symbol is the requested stock's symbol ('AAPL' for Apple)
# The response is JSON data of an array composed of "snapshot" objects (date + stock info + ...), usually one per day
def single_stock_historic(request, symbol):
    data = stock_api.get_stock_historic_prices(symbol, time_range='1m')
    return JsonResponse({'data': data})
