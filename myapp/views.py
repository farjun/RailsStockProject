from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from myapp import stock_api
from myapp.forms import  EditProfileForm, ProfileForm
from myapp.models import Stock,Profile

def index(request):
    """ View for the home page - a list of 20 of the most active stocks """
    # Query the stock table, filter for top ranked stocks and order by their rank.
    data = Stock.objects.filter(top_rank__isnull=False).order_by('top_rank')
    return render(request, 'index.html', {'page_title': 'Main', 'data': data })

def single_stock(request, symbol):
    """ View for the single stock page symbol is the requested stock's symbol ('AAPL' for Apple) """
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
    """ the user's profile view """
    return render(request, 'profile.html')

def register(request):
    """ the registration view of the project for creating users using UI """
    # If post -> register the user and redirect to main page
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        newuser = User.objects.create_user(username=username, email=email, password=password)
        newuser.first_name = firstname
        newuser.last_name = lastname
        newuser.save()
        return redirect('index')
    else:
        # If not post (regular request) -> render register page
        return render(request, 'register.html', {'page_title': 'Register'})

@login_required
def edit_profile(request):
    """ for editing the user's profile(in db) and updating his info depending on the entered values"""
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)  # request.FILES is show the selected image or file

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        args = {}
        # args.update(csrf(request))
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'edit_profile.html', args)

def logout_view(request):
    """ log the user out from his account and return him the home page"""
    logout(request)
    return redirect('index')

def single_stock_historic(request, symbol):
    """
    API for a stock's price over time
    symbol is the requested stock's symbol ('AAPL' for Apple)
    The response is JSON data of an array composed of "snapshot" objects (date + stock info + ...), usually one per day
    """
    data = stock_api.get_stock_historic_prices(symbol, time_range='1m')
    return JsonResponse({'data': data})
