from django.db.transaction import atomic
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

from oshop.api.models import Category, Products, ShoppingCart, CartDetails
from oshop.api.serializers import CategorySerializer, \
    ProductSerializer, \
    ShoppingCartSerializer, CartDetailsSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.exclude(id=1)
    serializer_class = CategorySerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer


class CartDetailsViewSet(viewsets.ModelViewSet):
    queryset = CartDetails.objects.all()
    serializer_class = CartDetailsSerializer


def update_cart(request, *args, **kwargs):
    cart_id = kwargs.pop('pk')
    product_id = kwargs.pop('productId')
    data = JSONParser().parse(request)
    carts = data['cart_details']
    shopping_cart = ShoppingCart.objects.get(id=cart_id)
    shopping_cart.amount = data['amount']
    cart_details = shopping_cart.cart_details.all()
    for item in cart_details:
        if item.product_id == product_id:
            item.qty += 1
            item.amount += data.carts['amount']
        else:
            new_carts = CartDetails
            new_carts.qty = 1
            new_carts.shopping_cart = cart_id
            new_carts.product = product_id
            new_carts.amount = carts['amount']
            new_carts.objects.create(shopping_cart=new_carts)
    shopping_cart.save()
    # cart_details.save()

    # shopping_cart.amount = data.amount

    return shopping_cart

