from itertools import product
from unicodedata import category
from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions, mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from saleapp.paginations import StandardResultsSetPagination
from .models import Category, Shipper, User, Order, Customer, Product, OrderDetail
from .serializers import CategorySerializers, CreateOrderDetailSerializers, ShipperSerializers, UserSerializers, OrderSerializers, ProductSerializers, OrderDetailSerializers


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializers
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current-user", detail=False)
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class ShipperViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Shipper.objects.all()
    serializer_class = ShipperSerializers
    parser_classes = [MultiPartParser, ]

    @action(methods=['get'], detail=False, url_path='orders')
    def get_orders(self, request):
        orders = Order.objects.all()
        return Response(OrderSerializers(orders, many=True, context={"request": request}).data,
                        status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    @action(methods=['get'], detail=True, url_path='products')
    def get_products(self, request, pk):
        category = self.get_object()
        products = Product.objects.filter(category=category)

        return Response(ProductSerializers(products, many=True, context={"request": request}).data,
                        status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializers

    @action(methods=['get'], detail=False, url_path='my-orders')
    def get_orders(self, request):
        orders = Customer.objects.get(user=request.user).orders

        return Response(OrderSerializers(orders, many=True, context={"request": request}).data,
                        status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        #---Custom the customer field = request.user when send request---#

        request.data._mutable = True
        request.data['customer'] = Customer.objects.get(user=request.user).id
        request.data._mutable = False
        print(request.data)

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['post'], url_path='change-status', detail=True)
    def change(self, request, pk):
        order = self.get_object()
        order.status = 'Complete'
        order.save()
        role = request.user.role

        if role == 'shipper':
            pass

        return Response(data=OrderSerializers(order, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class OrderDetailViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = OrderDetail.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateOrderDetailSerializers


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    pagination_class = StandardResultsSetPagination
