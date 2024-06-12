from django.db import models
from shop.models import CustomUser

# Create your models here.

class Recent_search(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    word=models.TextField()

    def __str__(self):
        return self.user.username
