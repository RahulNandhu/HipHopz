from django.contrib import admin
from .models import UserCart,Total_orders,Order,Bank

# Register your models here.

admin.site.register(UserCart)
admin.site.register(Bank)
admin.site.register(Order)
admin.site.register(Total_orders)
