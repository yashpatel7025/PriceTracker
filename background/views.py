from django.shortcuts import render
from django.http import HttpResponse

from background_task import background
from django.contrib.auth.models import User
from django.core.mail import send_mail
from pricetracker import settings
from track.models import Product
from track.views import ProductCreateView


@background(schedule=60)
def hello():
  all_products=Product.objects.all()
  for p in  all_products:
			myurl= p.product_url
			obj=AmazonBot()
			p.current_price=obj.get_price_only(myurl)#make list rather than variable ..we can accesss all previous 
		     										  #current_price through list 
			p.current_price=float(p.current_price)
			try:
				if p.current_price<=p.desire_price:
						print("ail")	
						subject='woohoo..! Price Dropped'
						message=f'Price Dropped for product {p.title}..Grab it now '
						from_email=settings.EMAIL_HOST_USER 
						print("ail")
						recipients_list=['yashpatel7025@gmail.com']
						print("before send")
						send_mail(subject, message, from_email,recipients_list)
						print("mail sent")
			except:
			 	print(f'price for product {p.title} is not validdddddddddddd ')  

def background_view(request):
	hello()
	#return  HttpResponse("hello world")


@background(schedule=20)
def kya():
	all_products=Product.objects.all()

	for index,p in  enumerate(all_products):
		print("--------{}------------".format(index))
		print(p)#it will print title bcoz we have returned self.title in models.py
		
		
		ProductCreateView.new_product(p,-1)

		
