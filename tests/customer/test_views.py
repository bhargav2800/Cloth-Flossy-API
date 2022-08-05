import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from seller.models import Product, Brand, Colour, Size
from customer.models import Reviews, Order, Invoice
from customer.views import ViewAllProducts


@pytest.mark.django_db
def test_view_all_products(client):
    factory = APIRequestFactory()
    cat_detail = ViewAllProducts.as_view({'get':'list'})
    request = factory.get('/customer/view_all_products/')
    response = cat_detail(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_view_product_detail_fail(customer_login_client):
    url = reverse('product_view', kwargs={'id':1})
    response = customer_login_client.get(url)
    assert response.status_code == 404
    assert response.data == {'msg': 'Product Does Not Exist !'}

@pytest.mark.django_db
def test_view_product_detail(customer_login_client, create_product):
    url = reverse('product_view', kwargs={'id':1})
    response = customer_login_client.get(url)
    assert response.status_code == 200\

@pytest.mark.django_db
def test_view_searched_product(client):
    url = reverse('search_view', kwargs={'search_value':'zudio'})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_trending_products(client):
    url = reverse('trending_product_view')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_cart(customer_login_client):
    url = reverse('view_cart')
    response = customer_login_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_to_cart(create_product, customer_login_client):
    url = reverse('add_to_cart', kwargs={'id':Product.objects.get(name='zudio pents').id})
    response = customer_login_client.post(url)
    assert response.status_code == 200
    assert response.data == {'msg': 'Product Added To Cart Successfully'}


@pytest.mark.django_db
def test_add_to_cart_conflict(create_product, customer_login_client):
    url = reverse('add_to_cart', kwargs={'id':Product.objects.get(name='zudio pents').id})
    customer_login_client.post(url)
    response = customer_login_client.post(url)
    assert response.status_code == 409
    assert response.data == {'msg': 'Product Already Exist in Your Cart'}


@pytest.mark.django_db
def test_update_cart(add_to_cart_product, customer_login_client):
    url = reverse('add_to_cart', kwargs={'id':Product.objects.get(name='zudio pents').id})
    payload = dict(
        added_quantity=2
    )
    response = customer_login_client.put(url, payload)
    assert response.status_code == 200
    assert response.data == {'msg': 'Product Quantity has been Updated Successfully'}


@pytest.mark.django_db
def test_update_cart_out_of_stock(add_to_cart_product, customer_login_client):
    url = reverse('add_to_cart', kwargs={'id':Product.objects.get(name='zudio pents').id})
    payload = dict(
        added_quantity=100
    )
    response = customer_login_client.put(url, payload)
    assert response.status_code == 400
    assert response.data == {'msg': 'Out Of Stock'}

@pytest.mark.django_db
def test_update_cart_Product_Not_Exists(create_product ,customer_login_client):
    url = reverse('add_to_cart', kwargs={'id':Product.objects.get(name='zudio pents').id})
    payload = dict(
        added_quantity=2
    )
    response = customer_login_client.put(url, payload)
    assert response.status_code == 404
    assert response.data == {'msg': 'Product Does Not Exist In Your Cart!'}


@pytest.mark.django_db
def test_remove_cart_Product(add_to_cart_product ,customer_login_client):
    url = reverse('add_to_cart', kwargs={'id':Product.objects.get(name='zudio pents').id})
    response = customer_login_client.delete(url)
    assert response.status_code == 200
    assert response.data == {'msg': 'Product Has Been Removed From Cart Successfully'}


@pytest.mark.django_db
def test_remove_cart_Product_does_not_exists(create_product, customer_login_client):
    url = reverse('add_to_cart', kwargs={'id':Product.objects.get(name='zudio pents').id})
    response = customer_login_client.delete(url)
    assert response.status_code == 404
    assert response.data == {'msg': 'Product Does Not Exist In Your Cart !'}




#  WishLIst

@pytest.mark.django_db
def test_view_wishlist(customer_login_client):
    url = reverse('view_wishlist')
    response = customer_login_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_to_wishlist(create_product, customer_login_client):
    url = reverse('WishlistCrud', kwargs={'id':Product.objects.get(name='zudio pents').id})
    response = customer_login_client.post(url)
    assert response.status_code == 200
    assert response.data == {'msg': 'Product Added To Wishlist Successfully'}


@pytest.mark.django_db
def test_add_to_wishlist_conflict(create_product, customer_login_client):
    url = reverse('WishlistCrud', kwargs={'id':Product.objects.get(name='zudio pents').id})
    customer_login_client.post(url)
    response = customer_login_client.post(url)
    assert response.status_code == 409
    assert response.data == {'msg': 'Product Already Exist in Your WishList'}



@pytest.mark.django_db
def test_remove_wishlist_Product(add_to_wishlist_product ,customer_login_client):
    url = reverse('WishlistCrud', kwargs={'id':Product.objects.get(name='zudio pents').id})
    response = customer_login_client.delete(url)
    assert response.status_code == 200
    assert response.data == {'msg': 'Product Has Been Removed From WishList Successfully'}


@pytest.mark.django_db
def test_remove_wishlist_Product_does_not_exists(create_product, customer_login_client):
    url = reverse('WishlistCrud', kwargs={'id':Product.objects.get(name='zudio pents').id})
    response = customer_login_client.delete(url)
    assert response.status_code == 404
    assert response.data == {'msg': 'Product Does Not Exist In Your WishList !'}









#  Reviews

@pytest.mark.django_db
def test_add_review(create_product, customer_login_client):
    url = reverse('product_reviews', kwargs={'id':Product.objects.get(name='zudio pents').id})
    payload = dict(
        review="not good product 5 star only"
    )
    response = customer_login_client.post(url, payload)
    assert response.status_code == 200
    assert response.data == {'msg': 'Product Review Added has Been Added Successfully'}


@pytest.mark.django_db
def test_add_review_not_exists(create_product, customer_login_client):
    payload = dict(
        review= "not good product 5 star only"
    )
    url = reverse('product_reviews', kwargs={'id':Product.objects.get(name='zudio pents').id+1})
    response = customer_login_client.post(url, payload)
    assert response.status_code == 404
    assert response.data == {'msg': 'Product Does Not Exists'}


@pytest.mark.django_db
def test_update_review(add_product_review,customer_login_client):
    payload = dict(
        review= "not good product 6 star only"
    )
    url = reverse('product_reviews', kwargs={'id':Reviews.objects.get(product__name='zudio pents').id})
    response = customer_login_client.put(url, payload)
    assert response.status_code == 200
    assert response.data == {'msg': 'Product Review Has been Updated Successfully'}


@pytest.mark.django_db
def test_update_review_not_exists(add_product_review,customer_login_client):
    payload = dict(
        review= "not good product 6 star only"
    )
    url = reverse('product_reviews', kwargs={'id':Reviews.objects.get(product__name='zudio pents').id+1})
    response = customer_login_client.put(url, payload)
    assert response.status_code == 404
    assert response.data == {'msg': 'Product Review Does Not Exist !'}


@pytest.mark.django_db
def test_delete_review(add_product_review,customer_login_client):
    url = reverse('product_reviews', kwargs={'id':Reviews.objects.get(product__name='zudio pents').id})
    response = customer_login_client.delete(url)
    assert response.status_code == 200
    assert response.data == {'msg': 'Product Review Has Been Deleted Successfully'}

@pytest.mark.django_db
def test_delete_review_not_exists(add_product_review,customer_login_client):
    url = reverse('product_reviews', kwargs={'id':Reviews.objects.get(product__name='zudio pents').id+1})
    response = customer_login_client.delete(url)
    assert response.status_code == 404
    assert response.data == {'msg': 'Product review Does Not Exist !'}


@pytest.mark.django_db
def test_fav_brands_view(add_product_review,customer_login_client):
    url = reverse('fav_brand_section', kwargs={'id':0})
    response = customer_login_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_fav_brand(brand, customer_login_client):
    url = reverse('fav_brand_section', kwargs={'id':Brand.objects.get(brand_name='Zudio').id})
    response = customer_login_client.post(url)
    assert response.status_code == 200
    assert response.data == {'msg': 'Brand has Been Added Successfully to favourite section'}

@pytest.mark.django_db
def test_add_fav_brand_already_exist(brand, customer_login_client):
    url = reverse('fav_brand_section', kwargs={'id':Brand.objects.get(brand_name='Zudio').id})
    customer_login_client.post(url)
    response = customer_login_client.post(url)
    assert response.status_code == 409
    assert response.data == {'msg': 'Brand Already Exist In Favourite Section !'}


@pytest.mark.django_db
def test_remove_fav_brand(add_fav_brand, customer_login_client):
    url = reverse('fav_brand_section', kwargs={'id':Brand.objects.get(brand_name='Zudio').id})
    response = customer_login_client.delete(url)
    assert response.status_code == 200
    assert response.data == {'msg': 'Brand Has Been Removed Successfully From Fav Section'}


@pytest.mark.django_db
def test_remove_fav_brand_not_exists(add_fav_brand, customer_login_client):
    url = reverse('fav_brand_section', kwargs={'id':Brand.objects.get(brand_name='Zudio').id+1})
    response = customer_login_client.delete(url)
    assert response.status_code == 404
    assert response.data == {'msg': 'Brand Does Not Exists in Fav Section!'}


@pytest.mark.django_db
def test_order_cod_empty(customer_login_client):
    url = reverse('order')
    response = customer_login_client.post(url)
    assert response.status_code == 204
    assert response.data == {'msg': 'Your Cart Is Empty ! '}


@pytest.mark.django_db
def test_order_cod(add_to_cart_product, customer_login_client):
    payload = dict(
        address="iukgcikcnd"
    )
    url = reverse('order')
    response = customer_login_client.post(url, payload)
    assert response.status_code == 200
    assert response.data == {'msg': 'Your Order Has Been Submited Successfully'}


@pytest.mark.django_db
def test_order_view(order, customer_login_client):
    url = reverse('order')
    response = customer_login_client.get(url)
    assert response.status_code == 200



@pytest.mark.django_db
def test_order_razorpay_empty(customer_login_client):
    url = reverse('order_razorpay')
    response = customer_login_client.post(url)
    assert response.status_code == 204
    assert response.data == {'msg': 'Your Cart Is Empty ! '}


@pytest.mark.django_db
def test_order_razorpay_cod(add_to_cart_product, customer_login_client):
    payload = dict(
        address="iukgcikcnd"
    )
    url = reverse('order_razorpay')
    response = customer_login_client.post(url, payload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_details(order, customer_login_client):
    url = reverse('vieworderdetails', kwargs={'id':Order.objects.all()[0].id})
    response = customer_login_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_order_details_not_exists(order, customer_login_client):
    url = reverse('vieworderdetails', kwargs={'id':Order.objects.all()[0].id+1})
    response = customer_login_client.get(url)
    assert response.status_code == 404
    assert response.data == {"msg":'Order Does Not Exist'}


@pytest.mark.django_db
def test_order_cancel_not_exists(order, customer_login_client):
    url = reverse('Cancelorder', kwargs={'id':Order.objects.all()[0].id+1})
    response = customer_login_client.put(url)
    assert response.status_code == 404
    assert response.data == {"msg":'Order Does Not Exist'}


@pytest.mark.django_db
def test_order_cancel(order, customer_login_client):
    url = reverse('Cancelorder', kwargs={'id':Order.objects.all()[0].id})
    response = customer_login_client.put(url)
    assert response.status_code == 200
    assert response.data == {'msg':'Order Has Been Cancled Successfullys'}


@pytest.mark.django_db
def test_return_order_view(order, customer_login_client):
    url = reverse('Return Products')
    response = customer_login_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_return_order_not_eligible(order, customer_login_client):
    url = reverse('return_products', kwargs={'id':Invoice.objects.all()[0].id})
    response = customer_login_client.post(url)
    assert response.data == {'msg': 'This Product is not elligible For Return'}
    assert response.status_code == 400

@pytest.mark.django_db
def test_return_order(order, customer_login_client):
    invoice = Invoice.objects.all()[0]
    invoice.status = 'Delivered'
    invoice.save()
    url = reverse('return_products', kwargs={'id': Invoice.objects.all()[0].id})
    payload=dict(
        returned_reason = "Not Good Quality"
    )
    response = customer_login_client.post(url, payload)
    assert response.data == {'msg':'Product Return Request Has Been Added Successfully'}
    assert response.status_code == 200

@pytest.mark.django_db
def test_return_order_not_exist(order, customer_login_client):
    url = reverse('return_products', kwargs={'id': Invoice.objects.all()[0].id+1})
    response = customer_login_client.post(url)
    assert response.data == {"msg": 'Product Has Been Not Ordered By you'}
    assert response.status_code == 404



# replace

@pytest.mark.django_db
def test_replace_order_view(order, customer_login_client):
    url = reverse('Replace Products')
    response = customer_login_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_replace_order_not_eligible(order, customer_login_client):
    url = reverse('replace_products', kwargs={'id':Invoice.objects.all()[0].id})
    response = customer_login_client.post(url)
    assert response.data == {'msg': 'This Product is not elligible For Replacement'}
    assert response.status_code == 400

@pytest.mark.django_db
def test_replace_order(order, customer_login_client):
    invoice = Invoice.objects.all()[0]
    invoice.status = 'Delivered'
    invoice.save()
    url = reverse('replace_products', kwargs={'id': Invoice.objects.all()[0].id})
    payload = dict(
        replacement_reason="jcebskecd",
        replace_product_color= Colour.objects.all()[0].id,
        replace_product_size= Size.objects.all()[0].id
    )
    response = customer_login_client.post(url, payload)
    assert response.data == {'msg':'Product Replace Request Has Been Added Successfully'}
    assert response.status_code == 200

@pytest.mark.django_db
def test_replace_order_not_exist(order, customer_login_client):
    url = reverse('replace_products', kwargs={'id': Invoice.objects.all()[0].id+1})
    response = customer_login_client.post(url)
    assert response.data == {"msg": 'Product Has Been Not Ordered By you'}
    assert response.status_code == 404