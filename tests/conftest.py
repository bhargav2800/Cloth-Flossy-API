import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient
from account.models import User,Customer,Brand
from seller.models import Category,Colour,Size
from account.views import get_tokens_for_user
from cloth_store_api.settings import BASE_DIR


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def customer():
    data = dict(
        email="28001398bhargav@gmail.com",
        username="bhargav",
        password="123456@As",
        password2="123456@As"
    )
    user = User.objects.create_user(**data)
    Customer.objects.create(user=user, email=user.email, mobile_no="+919662316938")
    return user


@pytest.fixture
def customer_login_client(customer, client):
    response = client.post(reverse('login_customer'), dict(email=customer.email, password='123456@As'))
    token = get_tokens_for_user(customer)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])
    return client


@pytest.fixture
def brand():
    data = dict(
        username="zudio_brand",
        email="zudio@gmail.com",
        password="123456@As",
        password2="123456@As",
    )
    user = User.objects.create_user(**data)
    user.is_staff = True
    user.save()
    Brand.objects.create(user=user, email=user.email, brand_name='Zudio')
    return user


@pytest.fixture
def brand_login_client(brand, client):
    response = client.post(reverse('login_brand'), dict(email=brand.email, password='123456@As'))
    token = get_tokens_for_user(brand)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token["access"])
    return client


@pytest.fixture
def create_product(brand_login_client):
    cat_id = Category.objects.create(name='pents')
    color_id = Colour.objects.create(colour='red')
    size_id = Size.objects.create(size='XL')
    image_file = os.path.join(BASE_DIR, 'media/card2.png')
    with open(image_file, 'rb') as img_file:
        mock_profile_image = SimpleUploadedFile('card.png', img_file.read(), content_type='multipart/form-data')
    payload = dict(
        name = "zudio pents",
        image = mock_profile_image,
        short_line = "jejswef",
        price = 1234,
        discount = 12,
        quantity = 23,
        description = "csbjdc",
        category = cat_id.id,
        size = size_id.id,
        color = color_id.id,
        return_replace_days = 5
    )
    responce = brand_login_client.post(reverse('product_seller'), payload)