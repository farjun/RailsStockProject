from django.contrib.auth.models import User
from django.db import models
from django import forms
from multiselectfield import MultiSelectField
import sqlite3




""" the Stock's model is used to create stocks for the project use """
class Stock(models.Model):
    symbol = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=64)
    top_rank = models.IntegerField(null=True)
    price = models.FloatField()
    change = models.FloatField(null=True)
    change_percent = models.FloatField()
    market_cap = models.FloatField(null=True)
    primary_exchange = models.CharField(null=True, max_length=32)

""" the user's profile model - created automatically by sending a signal when the user is created"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    # not working !!
    job = models.CharField(max_length=10, null=True, blank=True, default=None)
    # TODO : add more info fields
    STOCKS_CHOICES = ()
    dbconn = sqlite3.connect('db.sqlite3')
    cur = dbconn.cursor()

    cur.execute("SELECT name,symbol FROM myapp_stock")
    rows = cur.fetchall()
    stocks_choice = []
    for row in rows:
        stocks_choice.append(row)

    STOCKS_CHOICES = tuple(stocks_choice)
    my_stocks = models.CharField(max_length=50, blank=True,choices=STOCKS_CHOICES, default=STOCKS_CHOICES)
    dbconn.close()

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username
