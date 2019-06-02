import scrapy
from scrapyproject.items import ScrapyprojectItem
from track.models import Product
import re
from scrapyproject.spiders import autoscrap
from scrapyproject import pipelines
#README
#https://github.com/scrapy-plugins/scrapy-djangoitem<-----docuentation No1 of DjangoItem which connects Django and scrapy frameworks
#https://blog.theodo.fr/2019/01/data-scraping-scrapy-django-integration/<----ex..how to connect scrapy and django database
#https://doc.scrapy.org/en/0.24/topics/djangoitem.html <-----documenttaion NO2 of DjanoItem
#https://sqliteonline.com/<------awesome website to view your database file
class AutoScrap(scrapy.Spider):
	name="quotes"
	start_urls=[
   "your_scrap_url_here"
	]
    
	def __init__(self, *args, **kwargs):


		if kwargs.get('check'):
			self.check=1
			self.product_object=kwargs.get('product_object')
			self.url = self.product_object.product_url
			self.start_urls=[self.url]



			

			
		else:
			self.check=0

			self.url = kwargs.get('url')# We are going to pass these args from our django view.
			                            #we can pass whatever we like from jnago
			self.d_price = kwargs.get('d_price')
			print('2'*50)
			self.start_urls=[self.url]
			self.author=kwargs.get('author')
			#print('2end'*20)

			#print(self.url)
			#print(self.d_price)
			
	        # We are going to pass these args from our django view.
	        # To make everything dynamic, we need to override them inside __init__ method

	def parse(self,response):
		if self.check:
			item_obj=self.product_object

			try:
			    current_price= response.css('span#priceblock_ourprice::text').extract()
			    
			    print()
			    print(current_price)
			    print()
			    current_price=current_price[0]

			except Exception:
				import traceback
				traceback.print_exc()
				try:
					current_price=response.css('span#priceblock_dealprice::text')[0].extract()
				except:
					try:
						current_price=response.css('span#priceblock_saleprice::text')[0].extract()
					except :
						current_price = "Not available"

						
            

			
			if current_price != "Not available":
				try:
					#price = current_price.replace(",", "")
					non_decimal = re.compile(r'[^\d.]+')
					price = non_decimal.sub('', current_price)
					price=float(price)#exception occur if price is not covertable to float i.e 123.00.150.00
				except:
					price= -999

			else:#if it is "not avialable"
				price= -1.00
			'''print('+'*50)
			print(current_price)
			print('+'*50)'''

			print('old current price in database is ',self.product_object.current_price )
			print('old desire price in database ',self.product_object.desire_price )
			print('new scraped current price is ',price )
			
			self.product_object.current_price=price

			if price!=-999 and price!=-1.00:
				    self.product_object.save()
				    print("price changed ",self.product_object.current_price)


				    from django.core.mail import send_mail
				    from pricetracker import settings
				    try:

				    	if self.product_object.current_price<=self.product_object.desire_price:
				    		print("$$$$ mail $$$$")
				    		subject='woohoo..! Price Dropped'
				    		message=f'Price Dropped for product {self.product_object.title}..Grab it now {self.product_object.product_url}'
				    		from_email=settings.EMAIL_HOST_USER 
				    		recipients_list=['yashpatel7025@gmail.com']
				    		print("before send")
				    		send_mail(subject, message, from_email,recipients_list)
				    		print("mail sent")
				    except:
				    	print(f'price for product {p.title} is not validdddddddddddd ')  


			print('Yessssssss checkkkkkkk doneeeeeeeeeeee')
			print()

		else:
			print('5'*50)

			item_obj=ScrapyprojectItem()#this class has all field that are in my Product database

			
			import traceback
			try:

				m=response.xpath("//span[@id='productTitle']/text()").extract()
				print()
				print(m)
				print()
				m=m[0]
				
				item_obj['title']=m.strip()#removes spaces and \n we got in title
				p=response.css('div.imgTagWrapper img').xpath('@data-a-dynamic-image')[0].extract()
				p=p[2:(p[2:].find('"')+2)]
				item_obj['img_src']=p
				item_obj['desire_price']=self.d_price
				item_obj['product_url']=self.url
			except Exception:
				print("nnnnnnooooooooooooooooooooooooooooooooooooooooooo")
				traceback.print_exc()#we are using setup()to do the job of reactor()
				                     #so when something erroe occurs while scraping then it doesnt throw
				                     #errors on its own..directly cloae the spyder
				                     #we dont come to understand in terminal thatwhats goig wrong
				                     #coz we directly see that spyder is closed
				                     #so we added heare exception,it will throw error when occured on terminal
				
			

			
			item_obj['author']=self.author#this should be 'User' instance

			

			try:
				 current_price= response.css('span#priceblock_ourprice::text').extract()
				 print()
				 print(current_price)
				 print()
				 current_price=current_price[0]

			except Exception:
				import traceback
				traceback.print_exc()
				try:
					current_price=response.css('span#priceblock_dealprice::text')[0].extract()
				except:
					try:
						current_price=response.css('span#priceblock_saleprice::text')[0].extract()
					except :
						current_price = "Not available"



						

			if current_price != "Not available":
				try:
					non_decimal = re.compile(r'[^\d.]+')
					price = non_decimal.sub('', current_price)
					price=float(price)#exception occur if price is not covertable to float i.e 123.00.150.00
				except:
					price= -999

			else:#if it is "not avialable"
				price= -1.00
			'''print('+'*50)
			print(current_price)
			print('+'*50)'''
			
			
			item_obj['current_price']=price
			print("7"*50)
			obj=pipelines.ScrapyprojectPipeline()
	 
			obj.process_item(item_obj,'quotes')
			print(7*"okokk")
			yield item_obj



	    #after this yeild it will go automatically to pipelines.py and go to scrapyprojectPipeline and then gointo
        #process_item(self,item, spider)method.. scraped data you yield will assign to item..
        
            

        