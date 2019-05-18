from django.urls import path
from . import views
from .views import (ProductListView,
                    ProductCreateView,
                    ProductUpdateView,
                    ProductDeleteView,
                    UserProductListView,
                    )

urlpatterns = [
    path('',views.first_view,name='track-home'),
    path('all/', ProductListView.as_view(), name='track-list-all-products'),
    path('WhyToUse/', views.why, name='track-why'),
    path('benefits/', views.benefits, name='track-benefits'),
    path('announcements/', views.announce, name='track-announcements'),
    path('product/new/',  ProductCreateView.as_view(), name='product-create'),
    path('about/', views.about,name="track-about"),
    
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('user/<str:username>', UserProductListView.as_view(), name='user-products'),#route from base.html by Your products link

    #to understnd GET and POST methods
    #path('ok/',views.ok,name='ok'),
    #path('ok2/',views.ok2,name='ok2'),  
    #path('okjson/',views.okjson,name='okjson'),
    #path('okjson2/',views.okjson2,name='okjson2')'''
    #path('my/',views.my,name='my'),

]