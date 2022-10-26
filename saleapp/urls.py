from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(prefix='users', viewset=views.UserViewSet, basename='user')
router.register(prefix='shippers',
                viewset=views.ShipperViewSet, basename='shippers')
router.register(prefix='orders', viewset=views.OrderViewSet, basename='orders')
router.register(prefix='items',
                viewset=views.OrderDetailViewSet, basename='items')
router.register(prefix='products',
                viewset=views.ProductViewSet, basename='products')
router.register(prefix='categories',
                viewset=views.CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls))

]
