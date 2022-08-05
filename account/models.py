from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class UserManager(BaseUserManager):
  def create_user(self, email, username, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          username=username,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, username, password=None, **extra_fields):


      user = self.create_user(email,password=password,username=username,)
      user.is_superuser = True
      user.is_staff = True
      user.save(using=self._db)
      return user


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # For login now we will use Email insted of Username
    REQUIRED_FIELDS = ['username']
    objects = UserManager()


    def __str__(self):
        return self.email


class Customer(models.Model):
    gender_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10, choices=gender_choices, default='Female')
    email = models.EmailField(max_length=50, unique=True)
    mobile_no = PhoneNumberField(unique=True, null=True)
    avatar = models.ImageField(null=True, default="avatar.svg", upload_to='profile_picture')

    def __str__(self):
        return f"{self.name} + {self.email}"

class Brand(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.id} ---- {self.brand_name}"
