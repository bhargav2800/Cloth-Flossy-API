from django.contrib import admin
from .models import User,Customer,Brand
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('username',)}),
      ('Permissions', {'fields': ('is_superuser','is_staff')}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email','username' ,'password1', 'password2', 'is_staff', 'is_superuser'),
      }),
  )

# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)
admin.site.register(Customer)
admin.site.register(Brand)