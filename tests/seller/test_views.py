import json

import pytest
from django.urls import reverse
from seller.models import Product


@pytest.mark.django_db
def test_view_self_products(create_product, brand_login_client):
    url = reverse('view_self_products')
    response = brand_login_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_self_product_reviews(create_product, brand_login_client):
    url = reverse('view_product_reviews', kwargs={'id':Product.objects.all()[0].id})
    response = brand_login_client.get(url)
    assert response.status_code == 200




