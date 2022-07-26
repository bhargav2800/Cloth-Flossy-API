from rest_framework import serializers
from seller.models import Product
from .models import Cart, WishList, Reviews, Favourites, Order, Invoice, ReturnProducts, ReplaceProducts

class ViewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['review']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'

class FavouriteBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = '__all__'


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['address']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class ReturnProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnProducts
        fields = '__all__'


class ReturnReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnProducts
        fields = ['returned_reason']


class ReplaceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplaceProducts
        fields = '__all__'


class ReplaceReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplaceProducts
        fields = ['replacement_reason', 'replace_product_size', 'replace_product_color']