from django.urls import path
from .views import RegisterCustomer, LoginCustomer, ProfileCustomer, ChangePasswordCustomer, SendPasswordResetEmailCustomer, PasswordResetCustomer, RegisterBrand, LoginBrand, ProfileBrand

urlpatterns = [
    path('register_customer/', RegisterCustomer.as_view(), name='register_customer'),
    path('login_customer/', LoginCustomer.as_view(), name='login_customer'),
    path('profile_customer/', ProfileCustomer.as_view(), name='profile_customer'),
    path('change_password_customer/', ChangePasswordCustomer.as_view(), name='change_password_customer'),
    path('send-password-reset-email/', SendPasswordResetEmailCustomer.as_view(), name='send-password-reset-email'),
    # Will Call From Email URL After Submit...
    path('reset-password/<uid>/<token>/', PasswordResetCustomer.as_view(), name='reset-password'),

    path('register_brand/', RegisterBrand.as_view(), name='register_brand'),
    path('login_brand/', LoginBrand.as_view(), name='login_brand'),
    path('profile_brand/', ProfileBrand.as_view(), name='profile_brand'),
]