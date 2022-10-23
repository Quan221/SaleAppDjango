from django.contrib import admin
from .models import User, Customer, Category, Product, Order, OrderDetail
# Register your models here.


class OrderDetailAdmin(admin.ModelAdmin):
    model = OrderDetail


admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail, OrderDetailAdmin)
