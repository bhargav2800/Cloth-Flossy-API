from django.contrib import admin
from .models import User,Customer,Brand
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserModelAdmin(BaseUserAdmin):
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('username',)}),
      ('Permissions', {'fields': ('is_admin','is_staff')}),
  )


  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'username', 'password1', 'password2'),
      }),
  )


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)
admin.site.register(Customer)
admin.site.register(Brand)