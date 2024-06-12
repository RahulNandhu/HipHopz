from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator



# Create your models here.

gender_choices=(
    ('N','Not Specifying'),
    ('M','Male'),
    ('F','Female')
)

class CustomUser(AbstractUser):
    phone=models.IntegerField(blank=True,null=True,default='+091')
    gender=models.CharField(max_length=20,choices=gender_choices,default='N')
    profile=models.ImageField(upload_to='images/user_profile',default='images/default_pro.png',blank=True,null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name=models.CharField(max_length=80)
    cover=models.ImageField(upload_to='images/category',null=True,blank=True)
    desc=models.TextField()

    def __str__(self):
        return self.name

class Sub_Category(models.Model):
    name=models.CharField(max_length=80)
    cover=models.ImageField(upload_to='images/sub_category',null=True,blank=True)
    desc=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=80)
    cover=models.ImageField(upload_to='media/Product',blank=True,null=True)
    desc=models.TextField()
    sub_category=models.ForeignKey(Sub_Category,on_delete=models.CASCADE)
    stock=models.IntegerField()
    price=models.IntegerField()
    discount=models.IntegerField(default=0,validators=[MaxValueValidator(100), MinValueValidator(0)])
    availability=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def offer(self):
        return (round((self.price*(100-self.discount))/100))


    def __str__(self):
        return self.name


class Reviews(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    rating=models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    review=models.TextField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    likes=models.IntegerField(default=0)


class Slide(models.Model):
    name=models.ForeignKey(Sub_Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images/slide',blank=True,null=True)


    def __str__(self):
        return self.name.name
