from django.contrib import admin
from django.forms import fields
from .models import User, Customer, Category, Product, Order, OrderDetail, Shipper
from django.template.response import TemplateResponse
from django.db.models import Count, Sum, Q
from django.urls import path


# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    def get_urls(self):
        return [
            path('receipt-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):

        order = Order.objects.all()
        items = OrderDetail.objects.all()
        c = order.count()

        sum = items.aggregate(Sum('price'))

        stats = items \
            .values('product__name') \
            .annotate(sum=Sum('price'), count=Count('product')).order_by()

        stats2 = items \
            .values('created_date__month') \
            .annotate(sum=Sum('price')).order_by()

        if request.method == "POST" and request.POST['from_date'] and request.POST['to_date']:
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            items = OrderDetail.objects.filter(
                created_date__range=(from_date, to_date))
            sum = items.aggregate(Sum('price'))

            stats2 = items \
                .values('created_date__month') \
                .annotate(sum=Sum('price')).order_by()

            stats = items \
                .values('product__name') \
                .annotate(sum=Sum('price'), count=Count('product')).order_by()

            # order = Order.objects.filter(
            #     created_date__range=(from_date, to_date))
            # stats = Shipper.objects.annotate(
            #     receipts_count=Count('receipts', filter=Q(
            #         receipts__created_date__range=(from_date, to_date))),
            #     shipper_revenue=Sum('receipts__price', filter=Q(
            #         receipts__created_date__range=(from_date, to_date)))
            # ).values('id', 'user__first_name', 'receipts_count', 'shipper_revenue')
            # stats2 = order
            # .values('created_date__month')
            # .annotate(sum=Sum('order__item__price')).order_by()

        return TemplateResponse(request,
                                'admin/receipt-stats.html', {
                                    'count': c,
                                    'sum': sum,
                                    'stats2': stats2,
                                    'stats': stats

                                })


class OrderDetailAdmin(admin.ModelAdmin):
    model = OrderDetail


admin.site.register(User)
admin.site.register(Shipper)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
