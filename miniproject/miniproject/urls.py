from django.contrib import admin
from django.urls import path, include
from miniapp import views as miniapp_views


app_name = 'miniapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', miniapp_views.login),
    path('login_complete/', miniapp_views.login_complete),
    path('signup/', miniapp_views.signup),
    path('logout/', miniapp_views.logout, name='logout'),
    path('create_cat/', miniapp_views.create_cat),
    path('create_cat/<str:city>', miniapp_views.create_cat),
    path('upload_cat_img/',miniapp_views.upload_cat_img),
    path('', miniapp_views.home, name='home'),
    path('home/', miniapp_views.home),
    path('cat_gallery/', miniapp_views.cat_gallery),
    path('cat_gallery/<str:city>', miniapp_views.cat_gallery_city),
    path('gallery_show_all_cats/', miniapp_views.gallery_show_all_cats),
    path('cat_profile/<int:pk>/',miniapp_views.cat_profile, name='profile'),
    path('my_cat/<int:id>', miniapp_views.my_cat2),
    path('comment/<int:board_id>',miniapp_views.commentdelete, name = 'delete')
]