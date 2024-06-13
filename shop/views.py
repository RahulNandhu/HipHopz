from django.shortcuts import render,HttpResponse,redirect
from .models import CustomUser,Category,Product,Sub_Category,Reviews,Slide
import random
from django.contrib.auth import authenticate,login,logout
from search.models import Recent_search
from cart.models import Total_orders
from django.db.models import Q
from django.db.models import Max
from django.http import HttpResponseRedirect
from .forms import ReviewForm,EditProfileForm
from django. contrib import messages
import re
# Create your views here.

def Home(request):
    user=request.user
    if user.is_superuser:
        return redirect('shop:admin_home')
    else:
        cat=Category.objects.all()
        sl=Slide.objects.all()
        sub_mob=Sub_Category.objects.get(name='Mobiles')
        m=Product.objects.filter(sub_category=sub_mob)[:4]
        h_dis_mobile=m[0]
        for i in m:
            if h_dis_mobile.discount<i.discount:
                h_dis_mobile=i
        mob=Product.objects.filter(sub_category=sub_mob).exclude(id=h_dis_mobile.id)
        if len(mob)>4:
            mobiles=mob[:4]
        else:
            mobiles=mob

        Ni=Product.objects.filter(name='Nike')

        if len(Ni)>6:
            Nike=Ni[:6]
        else:
            Nike=Ni

        s=Sub_Category.objects.get(name='Sarees')
        s_pro=Product.objects.filter(sub_category=s)

        if len(s_pro)>6:
            sarees=s_pro[:6]
        else:
            sarees=s_pro

        if request.user.is_authenticated:
            if user.gender=='F':
                sub_cat=Sub_Category.objects.get(name="Women's Tops")
                you_may_like=Product.objects.filter(sub_category=sub_cat)
            elif user.gender=='M':
                sub_cat = Sub_Category.objects.get(name="Casual Shirts")
                you_may_like = Product.objects.filter(sub_category=sub_cat)
            else:
                sub_cat = Sub_Category.objects.get(name="Boy's and Girl's T-shirts")
                you_may_like = Product.objects.filter(sub_category=sub_cat)
        else:
            sub_cat = Sub_Category.objects.get(name="Boy's and Girl's T-shirts")
            you_may_like = Product.objects.filter(sub_category=sub_cat)

        if len(you_may_like)>4:
            rn=random.randrange(0,len(you_may_like)-5)
            yml=you_may_like[rn:rn+4]
        else:
            yml=you_may_like

        sfy_sub=Sub_Category.objects.get(name='Mobiles')
        sfy_p=Product.objects.filter(sub_category=sfy_sub)

        sfy1=sfy_p[2]

        if len(sfy_p)>3:
            sfy2=sfy_p[:2]
        else:
            sfy2=sfy_p

        all_products=Rec_items=Product.objects.all()
        try:
            s_word=Recent_search.objects.get(user=user)

            if s_word.word.upper() == 'MOBILES' or s_word.word.upper() == 'MOBILE' or s_word.word.upper() == 'PHONE' or s_word.word.upper() == 'PHONES':
                Rec_items_sub = Sub_Category.objects.get(name='Mobiles')
                Rec_items = Product.objects.filter(sub_category=Rec_items_sub)
            else:
                Rec_items = Product.objects.filter(Q(name__icontains=s_word.word) | Q(desc__icontains=s_word.word))


            if len(Rec_items)>4:
                random_number=random.randrange(0,len(Rec_items)-5)
                Rec_items = Rec_items[random_number:random_number+4]

            elif len(all_products)>4:
                Rec_items = Product.objects.all()[:4]

            elif len(all_products)<4 and len(Rec_items)>0:
                Rec_items=all_products
            else:
                Rec_items=''
        except:

            if len(all_products)>4:
                Rec_items = Product.objects.all()[:4]

            elif len(all_products)<4 and len(Rec_items)>0:
                Rec_items=all_products
            else:
                Rec_items=''

        top_deals=Total_orders.objects.all().order_by('quantity')[:6]

        context={'cat':cat,'slides':sl,'mobiles':mobiles,'h_dis_mobile':h_dis_mobile,'Nike':Nike,'sarees':sarees,'yml':yml,'sfy1':sfy1,'sfy2':sfy2,'ri':Rec_items,'td':top_deals}
        return render(request,template_name='Home.html',context=context)

def U_register(request):
    msg=''
    success=False
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pass']
        cp=request.POST['cpass']
        e=request.POST['email']
        g=request.POST['gender']
        f=request.POST['fname']
        l=request.POST['lname']
        ph=request.POST['phone']
        profile=request.FILES['profile']

        if p == cp:
            if len(p) < 8:
                msg='Password must contain 8 characters'
            elif not re.match("^[a-zA-Z0-9_]+$",u):
                msg='Username can only contain letters, numbers, and underscores.'
            else:
                new_user = CustomUser.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l,phone=ph, gender=g, profile=profile)
                new_user.save()
                msg = 'Registration completed'
                success=True
        else:
            msg='Passwords are not matching...'

    return render(request,template_name='register_form.html',context={'msg':msg,'success':success})
global l
l=[0]
def U_login(request):
    num = random.randrange(1000, 9999)
    global str_num
    str_num=str(num)
    l.append(str_num)
    msg=''

    if request.method=='POST':
        capt=request.POST['captcha']
        username=request.POST['Uname']
        password=request.POST['Pass']
        print(l)

        if capt==l[-2]:

            user=authenticate(username=username,password=password)
            if user and user.is_superuser==True:
                return Admin_home(request)
            elif user:
                l.clear()
                l.append(0)
                login(request,user)
                return Home(request)
            else:
                msg='Invalid password or username'
                return render(request, template_name='login_form.html', context={'cap': str_num, 'msg': msg})
        else:
            msg='Incorrect Captcha'
            return render(request, template_name='login_form.html', context={'cap': str_num, 'msg': msg})
    return render(request,template_name='login_form.html',context={'cap':str_num,'msg':msg})



def U_logout(request):
    logout(request)
    return U_login(request)


def Sub_cate(request,p):
    c=Category.objects.get(id=p)
    sc=Sub_Category.objects.filter(category=c)
    return render(request,template_name='Sub_Category_page.html',context={'sc':sc})


def Items(request,p):

    price_limit=Product.objects.aggregate(price_limit=Max('price'))['price_limit']
    min_discount=0
    fil_price=price_limit
    # price_limit=2000                                                          for price filtering
    if request.method=='POST':
        min_discount=request.POST['min-discount']
        fil_price=request.POST['max_price']

    sc=Sub_Category.objects.get(id=p)
    cate=sc.category.name                                                       # for sub_category
    sub_category_filter=Sub_Category.objects.filter(category__name=cate).exclude(name=sc.name)

    it=Product.objects.filter(sub_category=sc)
    it=it.filter(discount__gte=min_discount)
    it=it.filter(price__lte=fil_price)
    context={'items':it,'discount':min_discount,'fil_price':fil_price,'price_limit':price_limit,'sub_category_filter':sub_category_filter,'sub_category_filter_current':sc}
    return render(request,template_name='items.html',context=context)

def Details(request,p):
    pr = Product.objects.get(id=p)
    u = request.user
    re=Product.objects.filter(sub_category=pr.sub_category).exclude(id=p)
    trending=Total_orders.objects.all().order_by('quantity').exclude(product_id=p)
    try:
        user_review = Reviews.objects.get(product=pr, user=u)
    except:
        user_review=''
    if len(trending)>=5:
        trending=trending[::-1][:4]
    if len(re) >4:
        random_number=random.randrange(0,len(re)-4)
        related_items=re[random_number:random_number+4]
    else:
        related_items=re
    if request.method=='POST':
        try:
            rating=request.POST.get('rating',0)
        except:
            rating=0
        review=request.POST.get('item_review','')
        r=Reviews.objects.filter(product=pr)

        flag=False
        for i in r:
            if i.user == u:
                flag=True
                break
        if flag == False:
            rev = Reviews.objects.create(user=u, product=pr, rating=rating, review=review, likes=0)
            rev.save()
            messages.success(request,'Review added successfully')
        else:
            messages.success(request,'A review already exists; you can edit your response.')


    num_of_reviews=Reviews.objects.filter(product=pr)
    if len(num_of_reviews) >5:
        reviews = Reviews.objects.filter(product=pr)[5]
    else:
        try:
            reviews=Reviews.objects.filter(product=pr).exclude(user=u)
        except:
            reviews=Reviews.objects.filter(product=pr)

    offer=int(pr.price)-round((pr.price*(100-pr.discount))/100)


    context={'product':pr,'rr':len(num_of_reviews),'offer':offer,'reviews':reviews,'ri':related_items,'tr':trending,'u_review':user_review}
    return render(request,template_name='detail.html',context=context)

def Admin_home(request):
    return redirect('admin:index')
def Edit_Review(request,p):
    review=Reviews.objects.get(id=p)

    if request.method=='POST':
        review_form=ReviewForm(request.POST,request.FILES,instance=review)
        if review_form.is_valid():
            review_form.save()
            return Details(request,p=review.product.id)

    review_form=ReviewForm(instance=review)
    return render(request,template_name='review_edit.html',context={'review_form':review_form})


def About(request):
    return render(request,template_name='about.html')

def Edit_Profile(request):
    # edit profile
    user=request.user
    msg=''
    success=False
    if request.method=='POST':
        user_form=EditProfileForm(request.POST,request.FILES,instance=user)
        if user_form.is_valid():
            user_form.save()
            success=True

        return render(request, template_name='Edit_profile.html', context={'user_form': user_form, 'msg': msg,'success':success})
    user_form=EditProfileForm(instance=user)
    return render(request,template_name='Edit_profile.html',context={'user_form':user_form,'msg':msg,'success':success})
