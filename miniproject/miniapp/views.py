from re import template
from turtle import st
# from aiohttp import request
from django.shortcuts import redirect,render, get_object_or_404
from django.http import HttpResponse,JsonResponse
from matplotlib.style import use
from .models import Location, User,CatPhoto,Cat, UserHasCat, Feed, City
from django.utils import timezone
from rest_framework import viewsets
from django.views.generic import DetailView
from datetime import datetime

def home(request):
    return render(request, 'miniapp/home.html')

def cat_profile(request, pk):
    update =False
    cat_profile = get_object_or_404(Cat, pk=pk)
    img = CatPhoto.objects.filter(cat_id=pk)
    feed = Feed.objects.filter(cat=pk).order_by('-date_time')[:5]
    comments = CatBoard.objects.filter(cat = pk)
    user_has_cat = UserHasCat.objects.filter(user_no=request.session['no'])
    u_h_c = False
    for u in user_has_cat:
        if u.cat_id == pk:
            u_h_c = True

    ##comments merge
    current_user_id = request.session['id']
    current_user = User.objects.get(user_id=current_user_id)
    cat_info = Cat.objects.get(cat_id = int(pk))
    comments = CatBoard.objects.filter(cat = int(pk))
    ##
    if request.method == 'POST':
    #     update =False
    #     if request.POST.get('update') == "True":
    #         update=True
        if request.POST.get('datetimep'):
            dt = request.POST.get('datetimep')
            b= dt.split(" ")
            c=b[0].split("/")
            d=b[1].split(":")
            dtstr = c[2]+"-"+c[0]+"-"+c[1]
            if b[2] == "PM": d[0] = str(int(d[0])+12)
            if len(d[0]) ==1: dtstr = dtstr +" 0"+d[0]+":"+d[1]+":00.000000"
            else: dtstr = dtstr +" "+d[0]+":"+d[1]+":00.000000"
        
            feed = Feed(date_time = dtstr,
                        cat_id = cat_profile.cat_id,
                        user_no =User.objects.get(user_no=request.session['no']  ))
            feed.save()
            feed = Feed.objects.filter(cat=pk).order_by('-date_time')[:5]
        ##comment merge##
        if request.POST.get('board_text'):
            comment = CatBoard()
            comment.cat = cat_info
            comment.user_no = current_user
            comment.board_text = request.POST.get('board_text')
            comment.date_time = timezone.now()
            comment.save()
        ##
    return render(request, 'miniapp/cat_profile.html', context={
        'cat_photo' : img[0],
        'cat_id' : cat_profile.cat_id,
        'cat_name': cat_profile.cat_name,
        'cat_location' : cat_profile.location,
        'cat_status': cat_profile.status,
        'feed_timeline': feed,
        'user_has_cat':u_h_c,
        'update':update,
        'comments': comments,
        #comment merge##
        'user_name': current_user.user_name,
        'cat_info': cat_info.cat_name,
        'user' : current_user,
        'comments': comments,
        ##
        })
    
        
  
def login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')
        try: 
            m=User.objects.get(user_id=user_id, user_pw=user_pw)
            # c= City.objects.all()
            # context = {
            #     'object': m,
            #     'city':c
            # }
            request.session['id']=user_id
            request.session['no']=m.user_no
            
            return redirect('http://127.0.0.1:8000/login_complete/')
        except:
            message = {
                'message': "로그인 실패!"
            }
            return render(request, 'miniapp/login.html', message)
    else:
        return render(request, 'miniapp/login.html' )

def login_complete(request):
    if request.method == 'POST':

        request.session['city']= request.POST.get('location')
        print(request.session['city'])
        return redirect('http://127.0.0.1:8000/')
    else:
        m=User.objects.get(user_id=request.session['id'])
        c= City.objects.all()
        context = {
            'object': m,
            'city':c
        }
        return render(request, 'miniapp/login_complete.html', context)
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
        CatPhoto.objects.create(cat_photo=img,date_time=time,user_no_id=user.user_no,cat_id=cat.cat_id)
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
        ccc=zip(cat_list, cat_img)
        print(ccc)
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
    ccc=zip(cat_list, cat_img)
    print(cat_list)
    return render(request, 'miniapp/my_cat.html',  {'user':user,'cat_list':cat_list,'cat':zip(cat_list, cat_img)})


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

from .models import CatBoard
# def comment(request, cat_id):
#     current_user_id = request.session['id']
#     current_user = User.objects.get(user_id=current_user_id)
#     cat_info = Cat.objects.get(cat_id = int(cat_id))
#     comments = CatBoard.objects.filter(cat = int(cat_id))
#     if request.method == 'POST':
#         comment = CatBoard()
#         comment.cat = cat_info
#         comment.user_no = current_user
#         comment.board_text = request.POST.get('board_text')
#         comment.date_time = timezone.now()
#         comment.save()
#     return render(request, 'miniapp/comment.html', {
#         'user_name': current_user.user_name,
#         'cat_info': cat_info.cat_name,
#         'user' : current_user,
#         'comments': comments,
#         })


from django.contrib import messages
def commentdelete(request, board_id):
    current_user_id = request.session['id']
    current_user = User.objects.get(user_id=current_user_id)
    comment = CatBoard.objects.get(board_id = board_id)
    a = current_user.user_no
    b = comment.user_no
    c = comment.cat_id

    if a != b.user_no:
        messages.warning(request, '권한 없음')
    else:
        comment.delete()
    return redirect(f'/cat_profile/{c}/')    