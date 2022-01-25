from django.contrib import admin
from django.urls import path, include
from miniapp import views as miniapp_views
from rest_framework import routers
from django.contrib.auth import views as auth_views

app_name = 'miniapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', miniapp_views.login),
    path('signup/', miniapp_views.signup, name='signup'),
    path('create_cat/', miniapp_views.create_cat),
    path('signup_complete/', miniapp_views.signup_complete),
    path('login_complete/', miniapp_views.login_complete),
    path('upload_cat_img/',miniapp_views.upload_cat_img),
    path('show/', miniapp_views.show),
    path('show/<int:cat_id>', miniapp_views.show2),
    path('', miniapp_views.home),
    path('home/', miniapp_views.home),
    path('my_cat/', miniapp_views.my_cat),
    path('my_cat/<int:id>', miniapp_views.my_cat2),
    # path('login/',
    #     auth_views.LoginView.as_view(template_name='miniapp/login.html'),
    #     name='login'),
]