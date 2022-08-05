from datetime import datetime, timezone

from django.db import models
from seller.models import Product, Brand
from account.models import Customer
from seller.models import Colour,Size


class Reviews(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Review_id:{self.id}"


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_quantity = models.IntegerField(default=1)

    @property
    def get_total(self):
        total = float(self.product.discount_price()) * self.added_quantity
        return total

    def __str__(self):
        return f"{self.customer.email}"

class WishList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.email}"

class Favourites(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.email}  ----   {self.brand}"


class Order(models.Model):
    payment_status_choices = (
        ('SUCCESS', 'SUCCESS'),
        ('FAILURE', 'FAILURE'),
        ('PENDING', 'PENDING'),
    )
    order_status_choices = (
        ('PLACED', 'PLACED'),
        ('FAIL', 'FAIL'),
        ('CANCELED', 'CANCELED'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    total_amount = models.FloatField(null=True)
    payment_method = models.CharField(max_length=30, default='Cash On Delivery')
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    # related to razorpay
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=payment_status_choices, default='PENDING')
    order_status = models.CharField(max_length=20, choices=order_status_choices, default='PLACED')


    def __str__(self):
        return f"{self.id}     {self.customer.user}"

class Invoice(models.Model):
    status_choices = (
        ('Not Packed', 'Not Packed'),
        ('Ready For Shipment', 'Ready For Shipment'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
        ('Returned', 'Returned'),
        ('Replaced', 'Replaced'),
        ('Failed', 'Failed'),
    )

    # Order
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()
    brand_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    buy_price = models.FloatField()
    product_discount = models.IntegerField()
    product_size = models.CharField(max_length=10)
    product_color = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=status_choices, default='Not Packed')
    order_delivery_date = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.id} --  {self.order.id}"


class ReturnProducts(models.Model):
    status_refund = (
        ('Not Initiated', 'Not Initiated'),
        ('Initiated', 'Initiated'),
        ('Done', 'Done')
    )
    status_pickup = (
        ('Will Soon Pick Up the Product', 'Will Soon Pick Up the Product'),
        ('Pick Up Done', 'Pick Up Done')
    )

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    returned_date = models.DateTimeField()
    returned_reason = models.TextField()
    pick_up_date = models.DateTimeField(blank=True, null=True)
    pick_up_status = models.CharField(max_length=30, choices=status_pickup, default='Will Soon Pick Up the Product')
    refund_status = models.CharField(max_length=20, choices=status_refund, default='Not Initiated')


class ReplaceProducts(models.Model):
    status_pickup = (
        ('Will Soon Pick Up the Product', 'Will Soon Pick Up the Product'),
        ('Pick Up Done', 'Pick Up Done')
    )

    status_choices = (
        ('Not Packed', 'Not Packed'),
        ('Ready For Shipment', 'Ready For Shipment'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    )

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    replaced_date = models.DateTimeField()
    replacement_reason = models.TextField()
    replace_pickup_date = models.DateTimeField(blank=True, null=True)
    replace_pickup_status = models.CharField(max_length=30, choices=status_pickup, default='Will Soon Pick Up the Product')
    replace_delivery_date = models.DateTimeField(blank=True, null=True)
    replace_delivery_status = models.CharField(max_length=20, choices=status_choices, default='Not Packed')
    replace_product_size = models.ForeignKey(Size, on_delete=models.CASCADE)
    replace_product_color = models.ForeignKey(Colour, on_delete=models.CASCADE)
