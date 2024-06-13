from django.contrib.auth.urls import path
from . import views

app_name='shop'

urlpatterns=[
    path('',views.Home,name='home'),
    path('admin_home', views.Admin_home, name='admin_home'),
    path('register/',views.U_register,name='register'),
    path('login/', views.U_login, name='login'),
    path('logout/', views.U_logout, name='logout'),
    path('sub_cate/<int:p>',views.Sub_cate,name='category'),
    path('items/<int:p>', views.Items, name='items'),
    path('details/<int:p>',views.Details,name='details'),
    path('edit_review/<int:p>',views.Edit_Review,name='edit_review'),
    path('About_page', views.About, name='About'),
    path('Edit_profile', views.Edit_Profile, name='Edit_profile'),

]