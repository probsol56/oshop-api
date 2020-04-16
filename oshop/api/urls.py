from django.urls import path, include
from rest_framework.routers import DefaultRouter

from oshop.api import views

router = DefaultRouter()
router.register('products', views.ProductsViewSet)
router.register('categories', views.CategoryViewSet)
router.register('shopping-cart', views.ShoppingCartViewSet)
# router.register('shopping-cart/<int:pk>/items/<int:productId>', views.update_cart, basename='ShoppingCartViewSet')
router.register('cart-details', views.CartDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('shopping-cart/<int:pk>/items/<int:productId>/', views.update_cart)
    ]
