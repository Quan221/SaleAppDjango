from enum import Enum
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser


class StatusEnum(Enum):
    ToReceive = 'ToReceive'
    Completed = 'Completed'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class PayMentMethod(Enum):
    Momo = 'Momo'
    COD = 'COD'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Role(Enum):
    Customer = 'Customer'
    Shipper = 'Shipper'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m', blank=True)
    role = models.CharField(
        max_length=50, choices=Role.choices(), default=Role.Customer.value)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, default='', blank=True)

    def __str__(self):
        return self.user.username

class Shipper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank_account = models.CharField(max_length=20, default='', blank=True)

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

    def __str__(self):
        return self.name


class Product(ModelBase):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='products/%Y/%m', null=True)
    price = models.FloatField(null=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders")
    ship_address = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=30, choices=StatusEnum.choices(), default=StatusEnum.ToReceive.value)
    payment_method = models.CharField(
        max_length=30, choices=PayMentMethod.choices(), default=PayMentMethod.COD.value)

    def __str__(self):
        return '''Đơn hàng thứ''' + ' ' + self.id.__str__()


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order, related_name='item', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return self.product.name + ' So luong: ' + str(self.quantity)
