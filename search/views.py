from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
from .models import Recent_search

# Create your views here.

def search(request):
    word=''
    result=None

    if request.method=='POST':
        word=request.POST['search']
        user=request.user
        if word:
            result=Product.objects.filter(Q(name__icontains=word) | Q(desc__icontains=word))
            try:
                RS=Recent_search.objects.get(user=user)
                RS.word=word
                RS.save()
            except:
                RS=Recent_search.objects.create(user=user,word=word)
                RS.save()

    return render(request,template_name='search.html',context={'re':result,'word':word})

def Search_without(request):
    word = ''
    result = None

    if request.method == 'POST':
        word = request.POST['search']
        user = request.user
        if word:
            result = Product.objects.filter(Q(name__icontains=word) | Q(desc__icontains=word))

    return render(request, template_name='search.html', context={'re': result, 'word': word})
