from django.urls import path, include
from . import views
from rest_framework import routers



router = routers.DefaultRouter()
router.register(prefix='users', viewset=views.UserViewSet, basename='user')
router.register(prefix='orders', viewset=views.OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls))

]