from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    pid=models.TextField()
    brand=models.TextField()
    name=models.TextField()
    dis=models.TextField()
    price=models.IntegerField()
    offer_price=models.IntegerField()
    stock=models.IntegerField()
    img=models.FileField()
    
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()

class Buy(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()
    price=models.IntegerField()
    data=models.DateField(auto_now_add=True)

class Contact(models.Model):
    name = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()


