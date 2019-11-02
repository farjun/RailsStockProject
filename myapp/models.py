from django.contrib.auth.models import User
from django.db import models
<<<<<<< HEAD
=======
from django import forms
from multiselectfield import MultiSelectField
>>>>>>> master
import sqlite3

STOCKS_CHOICES = ()
DATABASE_NAME = 'db.sqlite3'
STOCKS_DATABASE ='myapp_stock'
class Stock(models.Model):
<<<<<<< HEAD
    """ the Stock's model is used to create stocks for the project use """
=======
>>>>>>> master
    symbol = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=64)
    top_rank = models.IntegerField(null=True)
    price = models.FloatField()
    change = models.FloatField(null=True)
    change_percent = models.FloatField()
    market_cap = models.FloatField(null=True)
    primary_exchange = models.CharField(null=True, max_length=32)


class Profile(models.Model):
<<<<<<< HEAD
    """ the user's profile model - created automatically by sending a signal when the user is created"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    job = models.CharField(max_length=20, null=True, default=None)

    dbconn = sqlite3.connect(DATABASE_NAME)
    cur = dbconn.cursor()

    cur.execute("SELECT symbol,name FROM {}".format(STOCKS_DATABASE))
    rows = cur.fetchall()
    stocks_choice = []
    for row in rows:
        stocks_choice.append(row)

    STOCKS_CHOICES = tuple(stocks_choice)
    my_stocks = models.CharField(max_length=50, blank=True,choices=[choice for choice in STOCKS_CHOICES], default=[choice for choice in STOCKS_CHOICES])
    dbconn.close()

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username
=======

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')

    some_field = models.CharField(max_length=255, null=True, blank=True, default=None)
    # not working !!
    job = models.CharField(max_length=100, null=True, blank=True, default=None)

    dbconn = sqlite3.connect('db.sqlite3')
    cur = dbconn.cursor()

   # cur.execute("SELECT name,symbol FROM myapp_stock")

    rows = cur.fetchall()


    stocks_choice = []

    for row in rows:

        # row = str(row)

        # row.replace("(", "")
        stocks_choice.append(row)

    STOCKS_CHOICES = tuple(stocks_choice)


    my_stocks = models.CharField(max_length=100, blank=True,choices=STOCKS_CHOICES, default="empty list")
    dbconn.close()


    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

>>>>>>> master
