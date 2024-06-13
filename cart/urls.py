from django.urls import path
from . import views
app_name='cart'

urlpatterns=[
    path('usercart',views.Cart,name='usercart'),
    path('addtocart/<int:p>', views.Addtocart, name='addtocart'),
    path('removecart/<int:p>', views.Removecart, name='removecart'),
    path('deletecart/<int:p>', views.Deletecart, name='deletecart'),
    path('singleorder/<int:p>', views.Single_order, name='singleorder'),
    path('order',views.Orders,name='order'),
    path('ordered',views.Ordered_items,name='ordered'),
    path('buy_now/<int:p>',views.Buy_now,name='buy_now'),

]