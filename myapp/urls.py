from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

""" we add the path (the url to redirect the user to) of every view """
urlpatterns = [
	path('', views.index, name='index'),
	path('stock/<str:symbol>/', views.single_stock, name='single_stock'),
	path('historic/<str:symbol>/', views.single_stock_historic, name='single_stock_historic'),
	path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	path('accounts/logout/', views.logout_view, name='logout'),
	path('accounts/register/', views.register, name='register'),
	path('accounts/profile/', views.profile, name='profile'),
<<<<<<< HEAD
	path('accounts/profile/edit/', views.edit_profile, name='edit_profile'),

]
=======
	path('accounts/profile/edit', views.edit_profile, name='edit_profile'),

]

>>>>>>> master
if settings.DEBUG:
	urlpatterns += static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
