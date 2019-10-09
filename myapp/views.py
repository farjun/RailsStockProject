from django.shortcuts import render, redirect
from myapp import stock_api
from myapp.models import Stock
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.generic import View



# View for the home page - a list of 20 of the most active stocks
def index(request):
	# Query the stock table, filter for top ranked stocks and order by their rank.
	data = Stock.objects.filter(top_rank__isnull=False).order_by('top_rank')
	return render(request, 'index.html', {'page_title': 'Main', 'data': data })


# View for the single stock page
# symbol is the requested stock's symbol ('AAPL' for Apple)
def single_stock(request, symbol):
	data = stock_api.get_stock_info(symbol)
	return render(request, 'single_stock.html', {'page_title': 'Stock Page - %s' % symbol, 'data': data})

def two_stocks(request, symbol1,symbol2):
	data1 = stock_api.get_stock_info(symbol1)
	data2 = stock_api.get_stock_info(symbol2)
	return render(request, 'compareTemp.html', {'data1': data1,'data2':data2})



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

def single_stock_financial(request, symbol):
	data = stock_api.get_financial_info(symbol)
	return render(request,'financial.html',{'data': data})


class CompareView(View):
    def post(self, request):
        symbol1 = request.POST['symbol1']
        symbol2 = request.POST['symbol2']

        stock1 = stock_api.get_financial_report(symbol1)
        stock2 = stock_api.get_financial_report(symbol2)

        return JsonResponse([stock1, stock2])

    def get(self, request):
        return render(request, 'compare.html')








