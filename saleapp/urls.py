from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(prefix='users', viewset=views.UserViewSet, basename='user')
router.register(prefix='orders', viewset=views.OrderViewSet, basename='orders')
router.register(prefix='detail',
                viewset=views.OrderDetailViewSet, basename='detail')
router.register(prefix='products',
                viewset=views.ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls))

]
