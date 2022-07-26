from django.contrib import admin
from .models import Cart,Reviews,Favourites,WishList, Order, ReturnProducts, ReplaceProducts, Invoice

admin.site.register(Cart)
admin.site.register(Reviews)
admin.site.register(Favourites)
admin.site.register(WishList)
admin.site.register(Order)
admin.site.register(Invoice)
admin.site.register(ReturnProducts)
admin.site.register(ReplaceProducts)