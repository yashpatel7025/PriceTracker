from django.shortcuts import render
from django.http import HttpResponse

from background_task import background
from django.contrib.auth.models import User
from django.core.mail import send_mail
from pricetracker import settings
from track.models import Product
from track.views import ProductCreateView


@background(schedule=60)
def run_task():
  all_products=Product.objects.all()
  for p in  all_products:
			myurl= p.product_url
			obj=AmazonBot()
			p.current_price=obj.get_price_only(myurl)#make list rather than variable ..we can accesss all previous 
		     										  #current_price through list 
			p.current_price=float(p.current_price)
			try:
				if p.current_price<=p.desire_price:	
						subject='woohoo..! Price Dropped'
						message=f'Price Dropped for product {p.title}..Grab it now '
						from_email=settings.EMAIL_HOST_USER 
						recipients_list=['yashpatel7025@gmail.com']
						send_mail(subject, message, from_email,recipients_list)
			except:
			 	pass  

def background_view(request):
	run_task()


@background(schedule=20)
def bg_task_run_view():
	all_products = Product.objects.all()
	for index,p in  enumerate(all_products):
		ProductCreateView.new_product(p,-1)

		
