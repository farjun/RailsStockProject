from django.db import models



# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=64)
    top_rank = models.IntegerField(null=True)
    price = models.FloatField()
    change = models.FloatField(null=True)
    change_percent = models.FloatField()
    market_cap = models.FloatField(null=True)
    primary_exchange = models.CharField(null=True, max_length=32) # NASDAQ

class User(models.Model):
    name = models.CharField(max_length=12)

class follow(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.PROTECT, null=True,  related_name='user')
    stock_id=models.ForeignKey(Stock,on_delete=models.PROTECT, null=True,  related_name='stock')