from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
from django.contrib.auth.models import User
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


from django.contrib import messages
from track.models import Product

from pricetracker import settings

from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from users.forms import UserRegisterForm

def home(request):
    context={

      'products':Product.objects.all(),
      'title':'Home'


    }
    return render(request,'track/home.html',context)#title is optional

class ProductListView(ListView):
    model = Product
    template_name = 'track/home.html'  # <app>/<model>_<viewtype>.html ...django searches for this covention template

    context_object_name = 'products'  #i dont understand where we defined this 'posts'...eariler home() was being called..there
                                    #'posts' was defined but now when we give route as blog/ it will come diretly to postview class 
                                    #we never defining  'posts':Post.objects.all(),.....but still it works
    ordering = ['-date_posted']
    paginate_by=5 #how mnay pages you want to show on home page

class ProductCreateView(LoginRequiredMixin,CreateView):#<app>/<model>_form.html ....this view follow this convention
                                                    #LoginRequiredMixin this is written bcoz user will see post form only if he 
                                                    #logged in otherwid=se if he try toa access that route blog/post/new then it will ask
                                                    #for login first
                                                    #we have done this ealier while showing profile and we had used decorators there..
                                                    #e cant use decorators with functions so we used it
    model = Product
    
   
    fields = ['product_url','desire_price']#this fields should be in your model Post
    context={

      'products':Product.objects.all(),
      'title':'Home'


    }

    def form_valid(self, form):
      f=self.new_product(form)
      if f==1:
          messages.success(self.request, f'Product Added successfully! We will notify you via email when price drop under your desire price')
          return HttpResponseRedirect(reverse('user-products', args=[self.request.user.username]))
      if f==0:
          messages.warning(self.request, f"Invalid URL or couldn't find proper price of product..try again")
          return HttpResponseRedirect(reverse('user-products', args=[self.request.user.username]))


    def new_product(self,form):

        from django.http import JsonResponse
        from django.views.decorators.csrf import csrf_exempt
        from scrapyd_api import ScrapydAPI
        from uuid import uuid4
        import time


        import sys
        #this path will remain in sys.path untill this program terminated
        sys.path.append("/app")
        sys.path.append("/app/scrapyproject")#in heroku we have base dir as /app
        sys.path.append("C:/Users/Aakash/Desktop/trackass/scrapyproject")#for testing in my local
                                                                                   #system
         #this path will be used in scrapyproject.items,                                                                          
        from scrapyproject.spiders import autoscrap
        from scrapyproject.pipelines import  ScrapyprojectPipeline

        from scrapy import signals
        from twisted.internet import reactor
        from scrapy.crawler import Crawler,CrawlerRunner,CrawlerProcess
        from scrapy.settings import Settings
        from scrapy.utils.project import get_project_settings 

        from crochet import setup#added this2 lines and removed reactor.run() and reacter().stop()
                              #since it was throwing error"Reactor not Restartable"after 2nd submission from 
                              #front end...first submission works but when we do 2nd then reactor is already 
                              #strated in first so you cant start it again since there is only one reactor in system
       

        #print(self.request.POST)
        


   
        
        setup()
        print('hello'*10)
        
        if form==-1: 
          
          url=self.product_url

          settings = {
                  'url':url,
                  'USER_AGENT': 'scrapyproject (+http://www.yourdomain.com)',
                  'timepass':'kya chal raha hai bhai'
              }

          def spider_closing(spider):
              """Activates on spider closed signal"""
              print("Spiderclose"*10)
              #reactor.stop()

          crawler = Crawler(autoscrap.AutoScrap,settings)
          
          crawler.signals.connect(spider_closing, signal=signals.spider_closed)

          p_obj=self

          crawler.crawl(product_object=p_obj,check=1)

          while True:
                time.sleep(1)
                #print(crawler.stats.get_stats())
                try:
                  fr=crawler.stats.get_stats()['finish_reason']
                  if fr=='finished':
                    break
                except:
                  pass

          

        else:
          print("we are in else part")
          url = self.request.POST['product_url']
          d_price = self.request.POST['desire_price']

        
          settings = {
                  'url':url,
                  'USER_AGENT': 'scrapyproject (+http://www.yourdomain.com)',
                  'timepass':'kya chal raha hai bhai'
              }

      
        


          def spider_closing(spider):
              """Activates on spider closed signal"""
              print("Spiderclose"*10)
              #import sys        #here as well, we can see both path on terminal added to sys.path ,
                                 #we added both in track.views.it will remain untill program terminated.
              #print(sys.path)
              #reactor.stop()
          def if_spyder_open(spider):
            print("spyderOpen__"*10)
        
       # settings = Settings()
       #settings.set("USER_AGENT", "Kiran Koduru (+http://kirankoduru.github.io)")
          u=self.request.user
          ulen1=len(u.product_set.all())

          crawler = Crawler(autoscrap.AutoScrap,settings)

          
          crawler.signals.connect(spider_closing, signal=signals.spider_closed)
          crawler.signals.connect(if_spyder_open,signal=signals.spider_opened)

          crawler.crawl(url=url,d_price=d_price,author=self.request.user,check=0,timepass='whats up..!!')

        
        #reactor.run()
          
          while True:
                print(crawler.stats.get_stats())
                time.sleep(1)
                #print(crawler.stats.get_stats())
                try:
                  fr=crawler.stats.get_stats()['finish_reason']
                  if fr=='finished':
                    break
                except:
                  pass
          ulen2=len(u.product_set.all()) #users total number of products in data base will increase here
                                         #after saving prodcut in database in pipeline.py
          if ulen2>ulen1:
             return 1
          elif ulen2==ulen1: #if it is remain equal it means something went wrong...either no proper price found
                                #or no proper url ..no proper price....then product will not store in database
                                #in pipeline.py
             return 0
       

        
          


        

        



###########################automation code for ProductCReateView############################3
'''def form_valid(self, form):#this 2 methods is completely ritten by me including that message .success but except return line
        #messages.success(self.request, f'Product Added successfully! We will notify you via email when price drop under your desrire price')
        form.instance.author = self.request.user
        f=self.new_product(form)
        if f==0:
            #if f==0...we dont want to save url and and desie pricetodata base
            return HttpResponseRedirect(reverse('user-products', args=[self.request.user.username]))
            #it takes me almost 2 hours to go to this route by just to write this link 
        elif f==1:
            return super().form_valid(form)#after this djangi will go to get_absolute_url()in  modules.py(if success_URLis not specified above..)and redirects to home page
             #super().form_valid(form) this will save our fields into database
    def new_product(self,form):
        myurl= form.instance.product_url
        obj=AmazonBot()
        #form.instance.title,form.instance.current_price,form.instance.img_src=obj.get_product_price_name_src(myurl)
        title,price,img=obj.get_product_price_name_src(myurl)#price is str
        
        if title==0 and price==0 and img==0:
            messages.warning(self.request, f'Invalid URL..plz enter proper URL')
            return 0
        else:
            try:
                price=float(price)#exception occur if price is not covertable to float i.e 123.00.150.00
                if type(price)==float: 
                    messages.success(self.request, f'Product Added successfully! We will notify you via email when price drop under your desrire price')
                    if price<=float(form.instance.desire_price):
                        messages.success(self.request, f'current price already meets your desire price')
                    form.instance.title=title
                    form.instance.current_price=price
                    form.instance.img_src=img
                    return 1
            except:
                 messages.warning(self.request,f"price not found..!plz select size of product ,then add URL(price is 890-1000 in this format)")
                 return 0'''






        
def about(request):

  return render(request,'track/about.html',{'title':'about '})#title is optional

def first_view(request):
  
  return render(request,'track/first_view.html')
def why(request):
 
  return render(request,'track/why.html')
def benefits(request):
  
  return render(request,'track/benefits.html')
def announce(request):
  
  return render(request,'track/announcements.html')



class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['title','desire_price']
    template_name = 'track/update_form.html'

    def form_valid(self, form):
        messages.success(self.request, f'Updated successfully!')
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):#this fucntion restric user to update others post..he can update only his own post not others
                        #UserPassesTestMixin thats why we write this 
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class UserProductListView(ListView):#when we click on title tis executed
    model = Product
    template_name = 'track/user_products.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))#this will get username presnet in
                                                                            #kwargs which is being
                                                                            #being passed from our route..if user is
                                                                            #not valid then error 404

        return Product.objects.filter(author=user).order_by('-date_posted')












#####################for understanding what is  GET and POST methods#################################
'''
from users.forms import UserRegisterForm
def ok(request):
    form = UserRegisterForm()
    myform={
         'form':form

        }

    if request.method == 'POST':
      print('*'*50)
      print(request.POST)
      email=request.POST['email']#we take data enter by user from front end by post request 
      print(email)
      print("okkkkkkkkkkkkkkkkkkkkkkkk post method in OK1111")
      print('*'*50)
    elif request.method == 'GET':
        print('*'*50)
        print("GET method in OK11111")
        print('*'*50)
    return render(request,'track/ok.html',myform)

def ok2(request):

    if request.method == 'POST':
      print(request.POST)
      print('*'*50)
      print("helllllloooo post method in OK2222")
      print('*'*50)
    elif request.method == 'GET':
        print('*'*50)
        print('GET method in OK2222')
        print('*'*50)

def okjson(request):
    

    if request.method == 'GET':
        print('*'*50)
        print("GET in okjson1111")
        print('*'*50)
        return render(request,'track/okjson.html')


def okjson2(request):

    

    if request.method == 'POST':
         print('*'*50)
         print("POST in okjson222222")
         print(request.POST)
         print('*'*50)
    else:
        print("GET in okjson22222")
    return JsonResponse({'error': 'Missing  args'})
    
    if request.method == 'GET':
          print('hi'*50)
'''


##################testing function for ProductCreate VIew....this run perfectly as welll#######################
'''
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from uuid import uuid4
import time

def my(request):
    from crochet import setup#added this2 lines and removed reactor.run() and reacter().stop()
                              #since it was throwing error"Reactor not Restartable"after 2nd submission from 
                              #front end...first submission works but when we do 2nd then reactor is already 
                              #strated in first so you cant start it again since there is only one reactor in system
    setup()

    if request.method == 'POST':
        print(request.POST['firstname'])
        print(request.POST)
        url = 'https://www.flipkart.com/'
        unique_id = str(uuid4())
        settings = {
            'unique_id': unique_id, # unique ID for each record for DB
            'USER_AGENT': 'scrapyproject (+http://www.yourdomain.com)',
            'timepass':'kya chal raha hai bhai'
        }
    import sys
    sys.path.append("C:/Users/Aakash/Desktop/trackass/scrapyproject")
    from scrapyproject.spiders import autoscrap
    from scrapyproject.pipelines import  ScrapyprojectPipeline


    
    print("hii"*50)

    from scrapy import signals
    from twisted.internet import reactor
    from scrapy.crawler import Crawler,CrawlerRunner,CrawlerProcess
    from scrapy.settings import Settings
    from scrapy.utils.project import get_project_settings
    


    def spider_closing(spider):
        """Activates on spider closed signal"""
        print("close"*20)
        #reactor.stop()

    
    settings = Settings()
    print("whatthefuck"*100)

    
    settings.set("USER_AGENT", "Kiran Koduru (+http://kirankoduru.github.io)")
    crawler = Crawler(autoscrap.AutoScrap(url='hello',domain='whats up..!!'),settings)
    print("after crawler "*10)

    
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)
    print("after signal"*10)

    
    print('!'*200)
    
    print("#"*200)
    crawler.crawl(url='hello',domain='whats up..!!')
    #reactor.run()
    t=1
    while t!=10:
      t+=1
      print(crawler.stats.get_stats())
      time.sleep(1) 
    


    

    return JsonResponse({'task_id': 5, 'unique_id': 8, 'status': 'started' })'''





############FROM VIEWS.PY TO passing in scrapy project by running 6800 local host###########
'''
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from uuid import uuid4
import time
# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')


scrapyd = ScrapydAPI('http://localhost:6800')

@csrf_exempt
def my(request):
    if request.method == 'POST':
        url = 'https://www.flipkart.com/'
        unique_id = str(uuid4())
        settings = {
            'unique_id': unique_id, # unique ID for each record for DB
            'USER_AGENT': 'scrapyproject (+http://www.yourdomain.com)',
            'timepass':'kya chal raha hai bhai'
        }
        #from subprocess import call
        #call(["twistd", "-ny","scrapyd.tac"])
        print("fuck"*50)
        #https://pypi.org/project/python-scrapyd-api/<---scrpyAPI documentation
        task = scrapyd.schedule('default', 'quotes', 
            settings=settings, url=url,domain='domain nahi hai kuch')
        task_id=task
        while scrapyd.job_status('default', task_id) != 'finished':
          print( scrapyd.job_status('default', task_id))
          time.sleep(3)
        if scrapyd.job_status('default', task_id) == 'finished':
          print(scrapyd.job_status('default', task_id))

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })'''