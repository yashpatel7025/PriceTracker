from django.db import models
from django.urls import reverse
from PIL import Image#
# Create your models here.

from django.utils import timezone
from django.contrib.auth.models import User

from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

class Product(models.Model):
	title=models.CharField(max_length=500)
	#content=models.TextField()
	current_price=models.FloatField(max_length=30)
	product_url=models.URLField(max_length=1000)
	img_src=models.URLField(max_length=1000)
	desire_price=models.FloatField(max_length=30)
	date_posted=models.DateTimeField(default=timezone.now)
	author=models.ForeignKey(User,on_delete=models.CASCADE)
	

	def __str__(self):
		return self.title#whenever user print product object then its title will be printed
		                  #__str__ func returned string representation of object..

	'''def get_absolute_url(self):#after successful posting of new poduct  this funct will redirect to home page
		return HttpResponseRedirect(reverse('track-home'))'''

	def get_absolute_url(self):#after successful posting of new poduct  this funct will redirect to home page
		return reverse('user-products',args=[self.author.username])