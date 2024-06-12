from django.db import models
from shop.models import Product,CustomUser

# Create your models here.

class UserCart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)

    def sub_total(self):
        return self.quantity* (round(self.product.price*((100-self.product.discount)/100)))

    def no_offer(self):
        return self.quantity*self.product.price

    def Total_discount(self):
        return self.quantity * (round(self.product.price*((self.product.discount)/100)))

    def __str__(self):
        return self.product.name


class Bank(models.Model):
    Account_number=models.IntegerField()
    Balance=models.IntegerField()


    def __str__(self):
        return str(self.Account_number)


class Order(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    MRP=models.IntegerField()
    D_price=models.IntegerField()
    order_date=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(max_length=30,default='pending')
    delivery_status=models.CharField(max_length=30,default='pending')
    phone=models.IntegerField()
    address=models.TextField()

    def __str__(self):
        return self.user.username

class Total_orders(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    m_user=models.IntegerField(default=0)
    f_user=models.IntegerField(default=0)

    def __str__(self):
        return self.product.desc

