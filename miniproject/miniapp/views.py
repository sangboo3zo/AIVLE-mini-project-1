from re import template
from turtle import st
from aiohttp import request
from django.shortcuts import redirect,render, get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import Location, User,CatPhoto,Cat, UserHasCat, Feed
from django.utils import timezone
from rest_framework import viewsets
from django.views.generic import DetailView


def home(request):
    return render(request, 'miniapp/home.html')

def cat_profile(request, pk):
    cat_profile = get_object_or_404(Cat, pk=pk)
    img = CatPhoto.objects.filter(cat_id=pk)
    feed = Feed.objects.filter(cat=pk).order_by('-date_time')

    return render(request, 'miniapp/cat_profile.html', context={
        'cat_photo' : img[0],
        'cat_name': cat_profile.cat_name,
        'cat_location' : cat_profile.location,
        'cat_status': cat_profile.status,
        'feed_timeline': feed})
  
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
            request.session['no']=m.user_no
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

def logout(request):
    request.session.flush()
    return redirect('http://127.0.0.1:8000/') 

def upload_cat_img(request):
    if request.method == 'POST':
        img = request.FILES.get('img-file')
        time = timezone.now()
        user = User.objects.get(user_no=2)
        cat = Cat.objects.get(cat_id=42)
        CatPhoto.objects.create(cat_photo=img,date_time=time,user_no_id=1,cat_id=42)
        return redirect(upload_cat_img)
    return render(request, 'miniapp/upload_cat_img.html')


def create_cat(request):
    if request.method == 'POST':
        cat_name = request.POST.get('cat_name')
        gender = request.POST.get('gender')
        neutral = request.POST.get('neutral')
        location = Location.objects.get(location4 ="분당중앙공원")
        appearance = request.POST.get("appearance")
        status =request.POST.get('status')
        m = Cat(
             cat_name=cat_name, gender=gender, neutral=neutral, location=location, appearance=appearance, status=status)
        m.save()
        name = request.session['id']
        user = User.objects.get(user_id = name)
        cat = Cat.objects.last()  
        img = request.FILES.get('img-file')
        time = timezone.now()
        CatPhoto.objects.create(cat_photo=img,date_time=time,user_no_id=user.user_no,cat_id=c.cat_id)
        UserHasCat.objects.create(cat_id=cat.cat_id,user_no=user)
        return redirect('http://127.0.0.1:8000/my_cat/'+str(user.user_no))
    return render(request, 'miniapp/create_cat.html')

def my_cat(request):
    if request.method == 'POST':
        name = request.session['id']
        num= name = request.session['no']
        user=User.objects.get(user_id=name)
        user_has_cat = UserHasCat.objects.filter(user_no=num)
        cat_id_list=[i.cat_id for i in user_has_cat]
        cat_list = [Cat.objects.get(cat_id=i) for i in cat_id_list]
        cat_img = []
        print(cat_list)
        for i in cat_id_list:
            if CatPhoto.objects.filter(cat_id=i):
                img_url = CatPhoto.objects.filter(cat_id=i).first().cat_photo
                cat_img.append("https://aivle-s43.s3.ap-northeast-2.amazonaws.com/"+ str(img_url))
            else:
                cat_img.append("https://aivle-s43.s3.ap-northeast-2.amazonaws.com/no_cat_img.png")
    return render(request, 'miniapp/my_cat.html',  {'user':user,'cat':zip(cat_list, cat_img)})

def my_cat2(request,id):
    user=User.objects.get(user_no=id)
    user_has_cat = UserHasCat.objects.filter(user_no=id)
    cat_id_list=[i.cat_id for i in user_has_cat]
    cat_list = [Cat.objects.get(cat_id=i) for i in cat_id_list]
    cat_img = []
    for i in cat_id_list:
        if CatPhoto.objects.filter(cat_id=i):
            img_url = CatPhoto.objects.filter(cat_id=i).first().cat_photo
            cat_img.append(" https://aivle-s43.s3.ap-northeast-2.amazonaws.com/"+ str(img_url))
        else:
            cat_img.append("https://aivle-s43.s3.ap-northeast-2.amazonaws.com/no_cat_img.png")
    return render(request, 'miniapp/my_cat.html',  {'user':user,'cat':zip(cat_list, cat_img)})

def cat_gallery(request):
    name = request.session['id']

    u=User.objects.get(user_id=name)
    #img = CatPhoto.objects.filter(user_no=int(u.user_no))
    img = CatPhoto.objects.all()
    cat = Cat.objects.all()
    context = {
        'object': img,
        'user': int(u.user_no),
        #'cat': cat.cat_name
    }
    
    return render(request, 'miniapp/cat_gallery.html', context)