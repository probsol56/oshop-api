from django.db import models


class Category(models.Model):
    cat_name = models.CharField(max_length=200)
    parent_cat_id = models.IntegerField()
    description = models.TextField()
    cat_image = models.CharField(max_length=100)
    active = models.IntegerField()
    create_date = models.DateTimeField()

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.cat_name


def product_img_path(instance, filename):
    return 'images/products/{product}/{file}'.format(product=instance.product_name, file=filename)


class Products(models.Model):
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.ImageField(upload_to=product_img_path)
    sell_price = models.IntegerField()
    cost_price = models.IntegerField()
    discount_price = models.IntegerField()
    active = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    cat = models.ForeignKey(Category, models.DO_NOTHING)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.product_name


class ShoppingCart(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()

    class Meta:
        db_table = 'shopping-cart'

    def __int__(self):
        return self.amount


class CartDetails(models.Model):
    qty = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    shopping_cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE, related_name='cart_details')
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        db_table = 'cart-details'

    def _int_(self):
        return self.shopping_cart
