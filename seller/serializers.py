from rest_framework import serializers
from .models import Product
from customer.models import Reviews, ReplaceProducts, ReturnProducts, Invoice

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductUpdateDeleteViewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','image','short_line','price','discount','quantity','description','category','size','color', 'return_replace_days']

class ProductReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'


class UpdateInvoiceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['status']


class ReturnProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnProducts
        fields = '__all__'


class UpdateReturnOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnProducts
        fields = ['pick_up_date', 'pick_up_status', 'refund_status']


class ReplaceProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplaceProducts
        fields = '__all__'


class UpdateReplaceOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplaceProducts
        fields = ['replace_pickup_date', 'replace_pickup_status', 'replace_delivery_status', 'replace_product_size', 'replace_product_color']

