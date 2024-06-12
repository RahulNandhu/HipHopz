from django.contrib import admin
from .models import CustomUser,Category,Sub_Category,Product,Reviews,Slide

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Product)
admin.site.register(Reviews)
admin.site.register(Slide)





