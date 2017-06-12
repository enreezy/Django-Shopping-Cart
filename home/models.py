import datetime
from django.db import models
from django.utils import timezone


class Items(models.Model):
	itemname = models.CharField(max_length=200, blank='true')
	itemprice = models.CharField(max_length=200, blank='true')
	category = models.CharField(max_length=200, blank='true')
	image = models.FileField(upload_to='images', blank='true')

	class Meta:
		db_table = u'home_items'

	def __str__(self):
		return self.itemname


class Accounts(models.Model):
	username = models.CharField(max_length=200, blank='true')
	password = models.CharField(max_length=200, blank='true')