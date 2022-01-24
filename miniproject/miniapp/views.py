from turtle import st
from aiohttp import request
from django.shortcuts import redirect,render
from django.http import HttpResponse,JsonResponse
from .models import User,CatPhoto,Cat
from django.utils import timezone
from rest_framework import viewsets



def login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')
        try: 
            m=User.objects.get(user_id=user_id, user_pw=user_pw)
            context = {
                'object': m
            }
            request.session['id']=user_id
            return render(request, 'miniapp/login_complete.html', context )
        except:
            message = {
                'message': "로그인 실패!"
            }
            return render(request, 'miniapp/login.html', message)
    else:
        return render(request, 'miniapp/login.html' )


def signup(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        user_pw = request.POST.get('password1')
        user_name = request.POST.get('username')
        user_email = request.POST.get('email')
        m = User(
            user_id=user_id, user_pw=user_pw, user_name=user_name,user_email=user_email)
        m.date_joined = timezone.now()
        m.save()
        return render(request, 'miniapp/signup_complete.html' )
    else:
        return render(request, 'miniapp/signup.html' )

def signup_complete(request):
    return render(request, 'miniapp/signup_complete.html' )

def upload_cat_img(request):
    if request.method == 'POST':
        img = request.FILES.get('img-file')
        time = timezone.now()
        user = User.objects.get(user_no=2)
        cat = Cat.objects.get(cat_id=42)
        CatPhoto.objects.create(cat_photo=img,date_time=time,user_no_id=1,cat_id=42)
        return redirect(upload_cat_img)
    return render(request, 'miniapp/upload_cat_img.html')


def show(request):

    name = request.session['id']

    u=User.objects.get(user_id=name)
    img = CatPhoto.objects.filter(user_no=int(u.user_no))
    #img = CatPhoto.objects.all()
    context = {
        'object': img,
        'user': int(u.user_no),
        'name': name
    }
    
    return render(request, 'miniapp/show.html', context)

def create_cat(request):
    if request.method == 'POST':
        cat_name = request.POST.get('cat_name')
        appearance = request.POST.get("appearance")
        
    #     cat_name = request.POST.get('cat_name')
    #     gender = request.POST.get('gender')
    #     neutral = request.POST.get('neutral')
    #     location1 = request.POST.get('location1')
    #     location2 = request.POST.get('location2')
    #     location3 =request.POST.get('location3')
    #     appearance = request.POST.get('흰색')
    #     status =request.POST.get('status')
    #     m = Cat(
    #         cat_name=cat_name, gender=gender, neutral=neutral,location1=location1, location2=location2, location3=location3, appearance=appearance, status=status)
    #     m.save()
    return render(request, 'miniapp/create_cat.html')
   

def my_cat(request):
    user = User.objects.filter(user_no=1).values()
    cat = Cat.objects.all()
    return render(request, 'miniapp/my_cat.html',  {'user':user,'cat':cat})

def login_complete(request):
    # if request.method == 'POST':
    #     return render(request, 'miniapp/show.html' )
    return render(request, 'miniapp/login_complete.html' )