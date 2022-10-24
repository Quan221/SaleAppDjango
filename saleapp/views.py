from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions, mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import User, Order, Customer, Product, OrderDetail
from .serializers import UserSerializers, OrderSerializers, ProductSerializers, OrderDetailSerializers


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


class OrderViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializers

    @action(methods=['get'], detail=False, url_path='my-orders')
    def get_orders(self, request):
        orders = Customer.objects.get(user=request.user).orders

        # lessons = self.get_object().lessons.filter(active=True)
        # return Response(OrderSerializers.serializer_class(orders, context={'request': request}).data,
        #                     status=status.HTTP_200_OK)
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


class OrderDetailViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = OrderDetail.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderDetailSerializers


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
