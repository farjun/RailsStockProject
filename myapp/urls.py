from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('stock/<str:symbol>/', views.single_stock, name='single_stock'),
	path('historic/<str:symbol>/', views.single_stock_historic, name='single_stock_historic'),
	path('financial/<str:symbol>/', views.single_stock_financial, name='price'),
	path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	path('accounts/logout/', views.logout_view, name='logout'),
	path('accounts/register/', views.register, name='register'),
	path('compare/', views.CompareView.as_view(), name='register'),
	# path('compare/<str:symbol1>&<str:symbol2>', views.two_stocks, name='register'),
	# path('compare/<str:symbol1>&<str:symbol2>', views.two_stocks, name='register'),
	path('financial/', views.financial_using_ajax, name='price'),

]