from django.shortcuts import render, redirect
from myapp import stock_api
from myapp.models import Stock
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from myapp.models import Comment
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django import utils

from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator



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
	comments = Comment.objects.filter(stock_id = symbol)
	#check for currency type and add it to data
	for object in all_companies:
		if object['symbol'] == symbol:
			currency = object['currency']
			break

	data['currency'] = currency
	

	return render(request, 'single_stock.html', {'page_title': 'Stock Page - %s' % symbol, 'data': data, 'comments':comments})


def register(request):
	# If post -> register the user and redirect to main page
	if request.method == 'POST':
		firstname = request.POST.get('firstname')
		lastname = request.POST.get('lastname')
		email = request.POST.get('email')
		password = request.POST.get('password')

		newuser = User.objects.create_user(username=email, email=email, password=password)
		newuser.first_name = firstname
		newuser.last_name = lastname
		newuser.save()
		return redirect('index')
	else:
		# If not post (regular request) -> render register page
		return render(request, 'register.html', {'page_title': 'Register'})


def logout_view(request):
	logout(request)
	return redirect('index')


# API for a stock's price over time
# symbol is the requested stock's symbol ('AAPL' for Apple)
# The response is JSON data of an array composed of "snapshot" objects (date + stock info + ...), usually one per day
def single_stock_historic(request, symbol):
	data = stock_api.get_stock_historic_prices(symbol, time_range='1m')
	return JsonResponse({'data': data})

#add comments to a specific task
@csrf_protect
def add_stock_comment(request):
	
	if request.method == 'POST':
		
		if request.POST.get('name') and request.POST.get('content'):
			comment= Comment()
			comment.author = request.POST.get('name')
			comment.text= request.POST.get('content')
			comment.stock_id = request.POST.get('stock_symbol')
			symbol = request.POST.get('stock_symbol')
			
			comment.save()

			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



