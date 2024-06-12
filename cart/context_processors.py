from .models import UserCart

def Cart_Total(request):

    t = 0
    if request.user.is_authenticated:
        user=request.user
        try:
            cart_item=UserCart.objects.filter(user=user)
            for i in cart_item:
                t += i.quantity
        except:
            t = 0
    return {'cart_count':t}


