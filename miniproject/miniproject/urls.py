from django.contrib import admin
from django.urls import path, include
from miniapp import views as miniapp_views


app_name = 'miniapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', miniapp_views.login),
    path('signup/', miniapp_views.signup),
    path('logout/', miniapp_views.logout, name='logout'),
    path('create_cat/', miniapp_views.create_cat),
    path('upload_cat_img/',miniapp_views.upload_cat_img),
    path('', miniapp_views.home, name='home'),
    path('home/', miniapp_views.home),
    path('cat_gallery/', miniapp_views.cat_gallery),
    path('my_cat/', miniapp_views.my_cat),
    path('cat_profile/<int:pk>/',miniapp_views.cat_profile, name='profile'),
    path('my_cat/<int:id>', miniapp_views.my_cat2),
    path('comment/<int:cat_id>/',miniapp_views.comment, name = 'comment'),
    path('comment/<int:board_id>/delete',miniapp_views.commentdelete, name = 'delete'),

]