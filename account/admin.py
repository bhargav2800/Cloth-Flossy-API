from django.contrib import admin
from .models import User,Customer,Brand


# Now register the new UserModelAdmin...
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Brand)