
import decimal
from functools import total_ordering
import datetime
from math import prod
from turtle import mode
from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.
class Catagories(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
       return self.name
    class Meta:
        verbose_name_plural ='Catagories'
        ordering = ['name']


class Products(models.Model):
    brand = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    catagorie = models.ForeignKey(Catagories,on_delete=models.PROTECT,default="Free")
    digital = models.BooleanField(default=False,null=True,blank=True)
    images =models.ImageField(upload_to="images/",null=True,blank= True)
    def __str__(self):
       return self.brand    
    class Meta:
        verbose_name_plural ='Products'
        ordering = ['brand']
class Customer (models.Model):
    user = models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="profile_pic/",default='profile_pic/default.jpg')
    address =models.CharField(max_length=255)
    def __str__(self):
        return f'{self.user.username} - Profile'
    def __str__(self):
        return f'{self.user.username} - Profile'
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered =models.DateTimeField(auto_now_add=True)
    compelete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id =models.CharField(max_length=200,null =True)
    @property
    def vat(self):
        vat = self.get_cart_total * decimal.Decimal('1.05')
        return vat
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum ([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum ([item.quantity for item in orderitems])
        return total
    def __str__(self):
        return str(self.id) 
class OrderItem(models.Model):
    product = models.ForeignKey(Products,on_delete=models.SET_NULL,blank=True,null=True)
    order= models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)
    date_added =models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total= self.product.unit_price * self.quantity
        return total