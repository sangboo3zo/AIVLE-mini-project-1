#from aiohttp import request
from django.shortcuts import redirect,render, get_object_or_404
from django.http import HttpResponse,JsonResponse
from sympy import I
from .models import  User,CatPhoto,Cat, UserHasCat, Feed, City, Park, CatBoard
from django.utils import timezone

def home(request):
    return render(request, 'miniapp/home.html')

def cat_profile(request, pk):
    update =False
    #cat_profile = get_object_or_404(Cat, pk=pk)
    cat_profile= Cat.objects.get(cat_id=pk)
    profile =  CatPhoto.objects.filter(cat_id=pk).first()
    img = CatPhoto.objects.filter(cat_id=pk).order_by('-date_time')[:6]
    feed = Feed.objects.filter(cat=pk).order_by('-date_time')[:5]
    comments = CatBoard.objects.filter(cat = pk)
    user_has_cat= UserHasCat.objects.filter(user_no=request.session['no'])
    nickname = UserHasCat.objects.filter(user_no=request.session['no'],cat_id = pk).first()
    print(nickname)
    u_h_c = False
    for u in user_has_cat:
        if u.cat_id == pk:
            u_h_c = True
    current_user_id = request.session['id']
    current_user = User.objects.get(user_id=current_user_id)
    cat_info = Cat.objects.get(cat_id = int(pk))
    comments = CatBoard.objects.filter(cat = int(pk))

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
        if request.POST.get('board_text'):
            comment = CatBoard()
            comment.cat = cat_info
            comment.user_no = current_user
            comment.board_text = request.POST.get('board_text')
            comment.date_time = timezone.now()
            comment.save()
        ##status change##
        if request.POST.get('status') or request.POST.get('gender') or request.POST.get('neutral') or request.POST.get('appearance'):
            cat_info.status = request.POST.get('status')
            cat_info.gender = request.POST.get('gender')
            cat_info.neutral = request.POST.get('neutral')
            cat_info.appearance = request.POST.get('appearance')
            cat_info.save()
            return redirect(f'/cat_profile/{pk}/')
        ##
        
        if request.FILES.get('img-file'):
            img = request.FILES.get('img-file')
            time = timezone.now()
            CatPhoto.objects.create(cat_photo=img,date_time=time,user_no_id=request.session["no"],cat_id=pk)
            return redirect(f'/cat_profile/{pk}/')
    return render(request, 'miniapp/cat_profile.html', context={
        'cat_view' : img[0],
        'profile':profile,
        'cat_photo' : img,
        'cat' : cat_profile,
        'feed_timeline': feed,
        'user_has_cat':u_h_c,
        'update':update,
        'comments': comments,
        'user_name': current_user.user_name,
        'cat_info': cat_info.cat_name,
        'user' : current_user,
        'comments': comments,
        'park' : cat_profile.park.park,
        'nickname' : nickname,
        })
    
def detail_gallery(request, pk):
    img = CatPhoto.objects.filter(cat_id=pk)
    return render(request, 'miniapp/cat_detail_gallery.html', context={
        'detail_gallery' : img
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
        try:
            user_id = request.POST.get('id')
            user_pw = request.POST.get('password1')
            user_name = request.POST.get('username')
            user_email = request.POST.get('email')
            m = User(
                user_id=user_id, user_pw=user_pw, user_name=user_name,user_email=user_email)
            m.date_joined = timezone.now()
            m.save()
            return render(request, 'miniapp/signup_complete.html' )
        except:
            messages = "아이디가 이미 존재합니다"
            return render(request, 'miniapp/signup.html',{'message':messages} )
    else:
        return render(request, 'miniapp/signup.html' )


# def signup(request):
#     if request.method == 'POST':
#         try:
#             #User.objects.get(user_id=request.POST['user_id'])
#             return render(request,'miniapp/signup.html',{'error':'이미 사용된 ID입니다.'})

#         except:
#         except User.DoesNotExist:
#             user_id = request.POST.get('id')
#             user_pw = request.POST.get('password1')
#             user_name = request.POST.get('username')
#             user_email = request.POST.get('email')
#             if user_id=="" or user_pw=="" or user_name=="" or user_email=="":
#                 messages.warning(request,"빈 칸으로 제출할 수 없습니다.")
#                 return redirect("리다이렉트")            
#             m = User(
#                 user_id=user_id, user_pw=user_pw, user_name=user_name,user_email=user_email)
#             m.date_joined = timezone.now()
#             m.save()
#             return render(request,'miniapp/signup_complete.html')
#     else:
#         return render(request, 'miniapp/signup.html' )




def logout(request):
    request.session.flush()
    return redirect('http://127.0.0.1:8000/') 

def upload_cat_img(request,cat_id):
    user = User.objects.filter(user_no=request.session["no"])
    cat = Cat.objects.filter(cat_id=cat_id)
    if request.method == 'POST':
        user = User.objects.filter(user_no=request.session["no"])
        cat = Cat.objects.filter(cat_id=cat_id)
        img = request.FILES.get('img-file')
        time = timezone.now()
    
        CatPhoto.objects.create(cat_photo=img,date_time=time,user_no_id=request.session["no"],cat_id=cat_id)
        
        #return render(request, 'miniapp/upload_cat_img.html' ,{'user':user,'cat':cat })
        return redirect('http://127.0.0.1:8000/cat_profile/'+str(cat_id))
    return render(request, 'miniapp/upload_cat_img.html' ,{'user':user,'cat':cat })

def create_cat(request,city):
    park = Park.objects.filter(city=request.session['city'])
    if request.method == 'POST':
        cat_name = request.POST.get('cat_name')
        gender = request.POST.get('gender')
        neutral = request.POST.get('neutral')
        parkname = request.POST.get('park')
        location = Park.objects.get(park=parkname)
        print(location)
        appearance = request.POST.get("appearance")
        status =request.POST.get('status')
        m = Cat(
             cat_name=cat_name, gender=gender, neutral=neutral, park=location, appearance=appearance, status=status)
        m.save()
        name = request.session['id']
        user = User.objects.get(user_id = name)
        cat = Cat.objects.last()  
        img = request.FILES.get('img-file')
        time = timezone.now()
        CatPhoto.objects.create(cat_photo=img,date_time=time,user_no_id=user.user_no,cat_id=cat.cat_id)
        UserHasCat.objects.create(cat_id=cat.cat_id,user_no=user,cat_nickname = cat_name)
        return redirect('http://127.0.0.1:8000/my_cat/'+str(user.user_no))
    return render(request, 'miniapp/create_cat.html',{'park':park})

def my_cat2(request,id):
    if request.method == 'POST' :
        cat_delete_id =request.POST.get('cat_id')
        uhc = UserHasCat.objects.get(user_no = request.session['no'] , cat_id =cat_delete_id)
        uhc.delete()
    user=User.objects.get(user_no=id)
    user_has_cat = UserHasCat.objects.filter(user_no=id).values("cat_id")
    cat_list = Cat.objects.filter(cat_id__in = user_has_cat)
    cat_img=[]
    for i in user_has_cat:
        cat_img.append(CatPhoto.objects.filter(cat_id=i['cat_id']).first())
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



def cat_gallery_city(request,city):
    c = City.objects.get(city_name=city)
    park = Park.objects.filter(city_id=city)
    uhc = UserHasCat.objects.filter(user_no = request.session['no']).values("cat_id")
    cat = Cat.objects.exclude(cat_id__in = uhc).values("cat_id")
    cat2 = Cat.objects.exclude(status="실종").values("cat_id")
    cat3 = Cat.objects.exclude(status="사망").values("cat_id")
    cat_idx1= [int(i['cat_id']) for i in cat if i not in uhc]
    cat_idx2= [int(i['cat_id']) for i in cat2 if i not in uhc]
    cat_idx3= [int(i['cat_id']) for i in cat3 if i not in uhc]
    cat_list= list(set(cat_idx1) & set(cat_idx2) & set(cat_idx3))
    img = CatPhoto.objects.filter(cat_id__in = cat_list)
    # 내가 이미 등록되어있으면 x
    if request.method == 'POST':
        parkname = request.POST.get('park')
        park_o = Park.objects.get(park=parkname)
        cat4 = Cat.objects.filter(park=park_o).values("cat_id")
        cat_idx4= [int(i['cat_id']) for i in cat4 if i not in uhc]
        cat_list= list(set(cat_list) & set(cat_idx4))
        img = CatPhoto.objects.filter(cat_id__in = cat_list)
        
        return render(request, 'miniapp/cat_gallery_city.html', {'object': img,
            'park': park})
    return render(request, 'miniapp/cat_gallery_city.html', {'object': img,
            'park': park})


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

def cat_gallery(request):
    name = request.session['id']
    no = request.session['no']
    
    img = CatPhoto.objects.filter(user_no = no)
    cat = Cat.objects.all()
    context = {
        'object': img,
        'cat': cat,
        'name': name
    }
    return render(request, 'miniapp/cat_gallery.html', context)

def gallery_show_all_cats(request):
    
    name = request.session['id']
    cat = Cat.objects.filter(status="실종").values("cat_id")
    cat2 = Cat.objects.filter(status="사망").values("cat_id")
    img = CatPhoto.objects.exclude(cat_id__in = cat)&CatPhoto.objects.exclude(cat_id__in = cat2)
    print(img)
    context = {
        'object': img,
        'cat': cat,
        'name': name
    }
    return render(request, 'miniapp/gallery_show_all_cats.html', context)
