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
from django.db.models import Q
from myapp import notifications
import json
from celery.decorators import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task

# View for the home page - a list of 20 of the most active stocks
def index(request):
	"""This function returns the top 20 most active stocks or returns stocks based on
	the search field

	**Template:**

	:template:'myapp/templates/index.html'

	"""
	if request.GET.get('search'): # this will be GET now      
		search_text = request.GET.get('search') # do some research what it does
		
		items = Stock.objects.filter(Q(symbol__icontains=search_text)
		| Q(name__icontains=search_text))
		return render(request,"index.html",{'page_title': 'Main', 'data': items })
	else:
		data = Stock.objects.filter(top_rank__isnull=False).order_by('top_rank')
		return render(request, 'index.html', {'page_title': 'Main', 'data': data })
	
# View for the single stock page
# symbol is the requested stock's symbol ('AAPL' for Apple)
def single_stock(request, symbol):
	"""Returns stock's info and the related comments for this stock.

	**Template:**

	:template:'myapp/templates/signle_stock.html'
	"""

	with open('myapp/static/currencies.json', 'r') as f:
		currency_json_obj = json.load(f)

	data = stock_api.get_stock_info(symbol)
	comments = Comment.objects.filter(stock_id = symbol)
	#Getting stock's currency 
	currency = currency_json_obj[symbol]
	#adding currency key to data
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
	"""
	Returns JSON object for a specific stock.
	"""
	data = stock_api.get_stock_historic_prices(symbol, time_range='1m')
	return JsonResponse({'data': data})

#add comments to a specific task
@csrf_protect
def add_stock_comment(request):
	"""This function adds comments to Comments table for a specific stock .

	**Template:**

	:template:'myapp/templates/signle_stock.html'
	"""
	if request.method == 'POST':
		
		if request.POST.get('name') and request.POST.get('content'):
			comment= Comment()
			comment.author = request.POST.get('name')
			comment.text= request.POST.get('content')
			comment.stock_id = request.POST.get('stock_symbol')
			symbol = request.POST.get('stock_symbol')
			
			comment.save()

			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



		


