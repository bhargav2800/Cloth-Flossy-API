import datetime
from django.utils import timezone
from django.contrib import admin
from django.db import models
from account.models import Brand


# Create your models here.
class Colour(models.Model):
    colour = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.colour}  --  {self.id}"


class Size(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.size}  --  {self.id}"


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.name}  --  {self.id}"


class Product(models.Model):
    gender_choice = (
        ("Men", "Men"),
        ("Women", "Women"),
        ("Kids", "Kids"))
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField()
    short_line = models.CharField(max_length=40)
    price = models.FloatField()
    discount = models.IntegerField()
    target_audience = models.CharField(max_length=10, choices=gender_choice, default='Men')
    no_of_purchases = models.IntegerField(default=0)

    quantity = models.IntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Colour, on_delete=models.CASCADE)
    description = models.TextField()
    return_replace_days = models.IntegerField(default=0)

    def discount_price(self):
        return "{:.2f}".format(self.price - ((self.price * self.discount) / 100))
