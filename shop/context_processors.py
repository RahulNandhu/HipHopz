from .models import Category,Sub_Category

def Category_nav_links(request):
    CNL=Category.objects.all()
    return {'Category_links':CNL}