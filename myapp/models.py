from django.contrib.auth.models import User
from django.db import models
from django import forms
from multiselectfield import MultiSelectField
import sqlite3


# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=64)
    top_rank = models.IntegerField(null=True)
    price = models.FloatField()
    change = models.FloatField(null=True)
    change_percent = models.FloatField()
    market_cap = models.FloatField(null=True)
    primary_exchange = models.CharField(null=True, max_length=32)


class Profile(models.Model):

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

