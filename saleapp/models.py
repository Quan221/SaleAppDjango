from enum import  Enum
from django.db import models
from django.contrib.auth.models import AbstractUser

class StatusEnum(Enum):
    ToReceive='ToReceive'
    Completed='Completed'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)



class PayMentMethod(Enum):
    Momo='Momo'
    COD ='COD'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Role(Enum):
    Customer='Customer'
    Shipper='Shipper'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')
    role = models.CharField(max_length=50,choices=Role.choices())

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, default='', blank=True)

    def __str__(self):
        return self.user.username

class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(ModelBase):
    name = models.CharField(max_length=50)

class Product(ModelBase):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category,null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='products/%Y/%m', null=True)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ship_address = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.FloatField()
    quantity = models.IntegerField()
    discount = models.DecimalField(max_digits=3, decimal_places=1)


class Receipt(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=30,choices=StatusEnum.choices())
    payment_method = models.CharField(max_length=30,choices=PayMentMethod.choices())



