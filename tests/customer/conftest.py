import pytest
from django.urls import reverse
from seller.models import Product,Brand

@pytest.fixture
def add_to_cart_product(create_product, customer_login_client):
    url = reverse('add_to_cart', kwargs={'id': Product.objects.get(name='zudio pents').id})
    response = customer_login_client.post(url)


@pytest.fixture
def add_to_wishlist_product(create_product, customer_login_client):
    url = reverse('WishlistCrud', kwargs={'id': Product.objects.get(name='zudio pents').id})
    response = customer_login_client.post(url)


@pytest.fixture
def add_product_review(create_product, customer_login_client):
    payload = dict(
        review="not good product 5 star only"
    )
    url = reverse('product_reviews', kwargs={'id': Product.objects.get(name='zudio pents').id})
    response = customer_login_client.post(url, payload)


@pytest.fixture
def add_fav_brand(brand, customer_login_client):
    url = reverse('fav_brand_section', kwargs={'id': Brand.objects.get(brand_name='Zudio').id})
    response = customer_login_client.post(url)


@pytest.fixture
def order(add_to_cart_product, customer_login_client):
    payload = dict(
        address="iukgcikcnd"
    )
    url = reverse('order')
    response = customer_login_client.post(url, payload)

