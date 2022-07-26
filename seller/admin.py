from django.contrib import admin
from .models import Colour,Size,Product,Category

# Register your models here.
admin.site.register(Colour)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(Category)
