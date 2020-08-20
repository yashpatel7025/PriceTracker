# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html



import scrapy
from scrapy_djangoitem import DjangoItem
#you need to add sys.path  ..path to your django project to import our track.models file....directly
#we cannon import models.py bcoz it is in another folder and this items.py is in differnt folder
#once we add path  to folder having that models.py in sys.path ..our import models
#statement search in sys.path and it will find that models.py file
#once we add this and when program is over ...that path will automatically deleted ..so 
#we have to run everytime sys.path().append in order to add that path
#our python program searches in sys.path evrytime we import something
#we can check sys.paths by commandline 
#-->C:\Users\Aakash>where python
#C:\ProgramData\Anaconda3\python.exe
#-->C:\Users\Aakash>cd C:\ProgramData\Anaconda3
#then open python interpreter by python enter
#and import sys
#sys.path command will give all path



#similarly we have to add 'pricetracker.settings' in environment variables
#to access models.py file fromjango project
#we dont have access of this files if we dont set environment variable DJANGO_SETTINGS_MODULE
#we also have to django.setup() in settings to access models.py
#this path also gets deleted onec program is over
import sys
print('@'*50)
print(sys.path)


import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'pricetracker.settings'

from track.models import Product


#class ScrapyprojectItem(scrapy.Item): 
         #title = scrapy.Field()
         #price = scrapy.Field()
         # img_url = scrapy.Field()    
                                      #<-------class we use if not use dajngo database


  # items.py we use to store fields...its container which contains your items

    # define the fields for your item here like:
    # title = scrapy.Field()
    #price = scrapy.Field()
   # img_url = scrapy.Field()  #<------we dont write this here we directly store ito database




    #here we directly use our django database and store our item in to data base directly 
    #touse our database from django project first we need to connect or itegrate scrapy and jango with
    #package djangoitem 
    #documentation---->https://github.com/scrapy-plugins/scrapy-djangoitem
    #we have first install scrapy_djangoitem
    
class ScrapyprojectItem(DjangoItem): 
        print('1'*50)
        django_model = Product
    #by writing this now we have items here directly from database.....we are telling this that we dont 
    #want to use scrapy.fields()...insted i am using django model..and that model is Product()

    #now this class ScrapyprojectItem will have all fields that is in Product model.