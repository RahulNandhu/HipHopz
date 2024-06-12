from django.shortcuts import render
from .models import UserCart,Bank,Order,Total_orders
from shop.models import Product,CustomUser

# Create your views here.


def Cart(request):
    user=request.user
    pro=UserCart.objects.filter(user=user)
    d=0
    t=0
    pa=0
    Ni=0
    for i in pro:
        t=t+(i.product.price*i.quantity)
        d=d+i.quantity * (round(i.product.price*((i.product.discount)/100)))
        Ni += i.quantity
    pa+=(t-d)
    return render(request,template_name='cartpage.html',context={'cart_items':pro,'total':t,'dis':d,'pa':pa,'Ni':Ni})

def Addtocart(request,p):
    pr=Product.objects.get(id=p)
    user=request.user
    try:
        c = UserCart.objects.get(user=user, product=pr)
        if(pr.stock>0):
            c.quantity += 1
            c.save()
            pr.stock -= 1
            pr.save()
    except:
        c=UserCart.objects.create(user=user,product=pr,quantity=1)
        c.save()
        pr.stock -= 1
        pr.save()
    return Cart(request)


def Removecart(request,p):
    user=request.user
    prod=Product.objects.get(id=p)
    try:
        ite=UserCart.objects.get(user=user,product=prod)
        if ite.quantity<=1:
            ite.delete()
            prod.stock += 1
            prod.save()
        else:
            ite.quantity -=1
            ite.save()
            prod.stock +=1
            prod.save()
        return Cart(request)
    except:
        return Cart(request)

def Deletecart(request,p):
    user=request.user
    prod=Product.objects.get(id=p)
    try:
        ite=UserCart.objects.get(user=user,product=prod)
        prod.stock +=ite.quantity
        prod.save()
        ite.delete()
        return Cart(request)
    except:
        return Cart(request)


def Single_order(request,p):
    item=Product.objects.get(id=p)
    u=request.user
    ca=UserCart.objects.get(product=item,user=u)
    T=(ca.product.price*ca.quantity)
    D=ca.quantity * (round(ca.product.price*((ca.product.discount)/100)))
    B=T-D
    msg=''
    if request.method=='POST':
        Acc=request.POST['acc']
        phone=request.POST['phone']
        address=request.POST['address']

        try:
            acco=Bank.objects.get(Account_number=Acc)
            if acco.Balance >=B:
                acco.Balance=acco.Balance-B
                acco.save()
                msg='Order Placed Successfully'
                order=Order.objects.create(user=u,product=item,quantity=ca.quantity,MRP=T,D_price=B,order_status='Ordered',phone=phone,address=address)
                order.save()
                try:
                    t_order=Total_orders.objects.get(product=item)
                    t_order.quantity +=1
                    if u.gender=='M':
                        t_order.m_user +=1
                    elif u.gender=='F':
                        t_order.f_user +=1
                    t_order.save()
                    return Ordered_items(request)
                except:
                    if u.gender=='M':
                        t_order = Total_orders.objects.create(product=item,quantity=ca.quantity,m_user=1)
                        t_order.save()
                    elif u.gender=='F':
                        t_order = Total_orders.objects.create(product=item,quantity=ca.quantity,f_user=1)
                        t_order.save()
                    else:
                        t_order = Total_orders.objects.create(product=item, quantity=ca.quantity)
                        t_order.save()

                ca.delete()
                return Ordered_items(request)
            else:
                msg='Insufficient balance'
        except:
            msg='Invalid Bank details'

    #     acco = Bank.objects.get(Account_number=Acc)
    #     if acco.Balance >=B:
    #         acco.Balance=acco.Balance-B
    #         acco.save()
    #         msg='Order Placed Successfully'
    #         order=Order.objects.create(user=u,product=item,quantity=ca.quantity,MRP=T,D_price=B,order_status='Ordered',phone=phone,address=address)
    #         order.save()
    #         try:
    #             t_order=Total_orders.objects.get(product=item)
    #             t_order.quantity +=1
    #             if u.gender=='M':
    #                 t_order.m_user +=1
    #             elif u.gender=='F':
    #                 t_order.f_user +=1
    #             t_order.save()
    #         except:
    #             if u.gender=='M':
    #                 t_order = Total_orders.objects.create(product=item,quantity=ca.quantity,m_user=1)
    #                 t_order.save()
    #             elif u.gender=='F':
    #                 t_order = Total_orders.objects.create(product=item,quantity=ca.quantity,f_user=1)
    #                 t_order.save()
    #             else:
    #                 t_order = Total_orders.objects.create(product=item, quantity=ca.quantity)
    #                 t_order.save()
    #
    #         ca.delete()
    #     else:
    #         msg='Insufficient balance'
    # else:
    #     msg='Invalid Bank details'

    return render(request,template_name='single_order.html',context={'Bill':B,'Total':T,'Discount':D,'msg':msg})


def Orders(request):
    u=request.user
    ca = UserCart.objects.filter(user=u)
    T=0
    D=0
    B=0
    NI=0
    for i in ca:
        T += (i.product.price * i.quantity)
        D += i.quantity * (round(i.product.price * ((i.product.discount) / 100)))
        NI = NI+ i.quantity
    B += T - D
    msg = ''
    if request.method == 'POST':
        Acc = request.POST['acc']
        phone = request.POST['phone']
        address = request.POST['address']

        try:
            acco=Bank.objects.get(Account_number=Acc)
            if acco.Balance >= B:
                acco.Balance -=B
                acco.save()

                for i in ca:
                    To = (i.product.price * i.quantity)
                    Di = i.quantity * (round(i.product.price * ((i.product.discount) / 100)))
                    B=To-Di
                    msg = 'Order Placed Successfully'
                    order = Order.objects.create(user=u, product=i.product, quantity=i.quantity, MRP=To, D_price=B,order_status='Ordered', phone=phone, address=address)
                    order.save()

                    try:
                        t_order = Total_orders.objects.get(product=i.product)
                        t_order.quantity += i.quantity
                        if u.gender == 'M':
                            t_order.m_user += 1
                        elif u.gender == 'F':
                            t_order.f_user += 1
                        t_order.save()
                    except:
                        if u.gender == 'M':
                            t_order = Total_orders.objects.create(product=i.product, quantity=i.quantity, m_user=1)
                            t_order.save()
                        elif u.gender == 'F':
                            t_order = Total_orders.objects.create(product=i.product, quantity=i.quantity, f_user=1)
                            t_order.save()
                        else:
                            t_order = Total_orders.objects.create(product=i.product, quantity=i.quantity)
                            t_order.save()
                ca.delete()
            else:
                msg='Insufficient Balance'
        except:
            msg='Invalid Bank details'


    return render(request,template_name='order_page.html',context={'Total':T,'Dis':D,'Bill':B,'Ni':NI,'msg':msg})


def Ordered_items(request):
    u=request.user
    ite=Order.objects.filter(user=u)
    return render(request,template_name='Ordered.html',context={'ite':ite})


