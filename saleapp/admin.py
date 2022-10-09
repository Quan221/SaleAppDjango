from django.contrib import admin
from .models import User, Category, Product, Order, Receipt, OrderDetail
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Receipt)

