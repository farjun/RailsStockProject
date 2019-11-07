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
	primary_exchange = models.CharField(null=True, max_length=32)

#comment model
class Comment(models.Model):
	"""
	This is the comment model. It includes : stock, author, text and created_date.
	"""
	stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='comments')
	author = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return self.text
	
class Notification(models.Model):
	"""Notification model"""
	notification_id = models.AutoField(primary_key=True)
	stock = models.ForeignKey('Stock', on_delete=models.CASCADE, related_name='stock_symbol')
	message = models.TextField()
	read = models.BooleanField(default=False)
	created_date = models.DateTimeField(auto_now_add=True, blank=True)

