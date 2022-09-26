from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions, mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from .models import User
from .serializers import UserSerializers


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializers
    parser_classes = [MultiPartParser,]

    # def post(self, request, *args, **kwargs):
    #     username = request.data['username']
    #     password = request.data['password']
    #     email = request.data['email']
    #     first_name = request.data['first_name']
    #     last_name = request.data['last_name']
    #     avatar = request.data['avatar']
    #     User.objects.create(username=username, password=password, email=email, first_name=first_name,
    #                         last_name=last_name, avatar=avatar)
    #
    #
    #     return HttpResponse({'message': 'User created'}, status=200)
    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current-user", detail=False)
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={'request': request}).data,
                        status=status.HTTP_200_OK)

