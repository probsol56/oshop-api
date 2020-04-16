from django.db.transaction import atomic
from rest_framework import serializers

from oshop.api.models import Category, Products, ShoppingCart, CartDetails
from oshop.uploadImage import Base64ImageField


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'cat_name')


class ProductSerializer(serializers.ModelSerializer):
    image_url = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Products
        fields = ('id', 'product_name', 'description', 'image_url',
                  'sell_price', 'cost_price', 'discount_price', 'active', 'cat')


class CartDetailsSerializer(serializers.ModelSerializer):
    shopping_cart = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CartDetails
        fields = ('qty', 'shopping_cart', 'product', 'amount')

    # def update(self, instance, validated_data):
    #     cart_details = validated_data.pop('carts')
    #     for cart in cart_details:
    #         product_id = cart.product_id
    #         if cart.product_id == product_id:
    #             pass


class ShoppingCartSerializer(serializers.ModelSerializer):
    cart_details = CartDetailsSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = ('id', 'amount', 'cart_details')

    @atomic
    def create(self, validated_data):
        cart_data = validated_data.pop('cart_details')
        cart = ShoppingCart.objects.create(**validated_data)
        for carts in cart_data:
            CartDetails.objects.create(shopping_cart=cart, **carts)
        return cart

    @atomic
    def update(self, instance, validated_data):
        carts_data = validated_data.pop('cart_details')[0]
        item_exists = CartDetails.objects.filter(shopping_cart_id=instance.id,
                                                 product_id=carts_data['product'].id).first()

        if item_exists:
            add_qty = item_exists.qty+1
            add_amount = item_exists.amount+carts_data['amount']
            CartDetails.objects.filter(shopping_cart_id=instance.id,
                                       product_id=carts_data['product'].id).update(
                qty=add_qty,
                amount=add_amount)

        else:
            CartDetails.objects.create(qty=1,
                                       shopping_cart_id=instance.id,
                                       product_id=carts_data['product'].id,
                                       amount=carts_data['amount'])
        ShoppingCart.objects.filter(id=instance.id).update(amount=validated_data['amount'])
        return instance
