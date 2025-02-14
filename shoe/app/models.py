from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

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
    created_at = models.DateTimeField(default=now)


class Contact(models.Model):
    name = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.TextField()
    address=models.TextField()
    street=models.TextField()
    city=models.TextField()
    state=models.TextField()
    pincode=models.IntegerField()
    phone=models.IntegerField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')],
        default='Pending'
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"