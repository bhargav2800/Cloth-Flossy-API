import os
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from django.urls import reverse
from cloth_store_api.settings import BASE_DIR


@pytest.mark.django_db
def test_register_customer(client):
    payload = dict(
        username="bhargav_customer",
        email="28001398bhargav@gmail.com",
        password="123456@As",
        password2="123456@As"
    )

    url = reverse('register_customer')
    response = client.post(url, payload)

    assert response.status_code == 201
    assert response.data['msg'] == 'Registration Has Been Done Sucessfully !'


@pytest.mark.django_db
def test_register_customer_pass_not_match(client):
    payload = dict(
        username="bhargav_customer",
        email="28001398bhargav@gmail.com",
        password="123456@A",
        password2="123456@As"
    )

    url = reverse('register_customer')
    response = client.post(url, payload)

    assert response.status_code == 400
    assert response.data == {"non_field_errors": ["Password and Confirm Password doesn't match"]}


@pytest.mark.django_db
def test_login_customer(client, customer):
    payload = dict(
        email=customer.email,
        password= '123456@As',
    )

    url = reverse('login_customer')
    response = client.post(url, payload)


    assert response.data['msg'] == 'Login Success'
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_customer_fail(client, customer):
    payload = dict(
        email=customer.email,
        password= '123456@A',
    )

    url = reverse('login_customer')
    response = client.post(url, payload)

    assert response.data == {'errors': {'non_field_errors':['Email or Password is not Valid']}}
    assert response.status_code == 404


@pytest.mark.django_db
def test_view_customer_profile(customer_login_client):
    url = reverse('profile_customer')

    response = customer_login_client.get(url)

    assert response.status_code == 200

@pytest.mark.django_db
def test_update_customer_profile(customer_login_client):
    image_file = os.path.join(BASE_DIR, 'media/card2.png')
    with open(image_file, 'rb') as img_file:
        mock_profile_image = SimpleUploadedFile('card.png', img_file.read(), content_type='multipart/form-data')

    payload = dict(
        username = 'bhargav',
        name = 'Bhargav Patel',
        avatar = mock_profile_image,
        email = '28001398bhargav@gmail.com',
        gender = 'Male',
        age = 22,
        mobile_no = '+919662316938',
    )

    url = reverse('profile_customer')
    response = customer_login_client.put(url, payload)
    assert response.status_code == 200
    assert response.data == {'msg': 'Profile Updated Successfully'}


@pytest.mark.django_db
def test_delete_customer_profile(customer_login_client):
    url = reverse('profile_customer')
    response = customer_login_client.delete(url)
    assert response.status_code == 200
    assert response.data == {"message": "user delete Successfully"}



@pytest.mark.django_db
def test_change_customer_password(customer_login_client):
    url = reverse('change_password_customer')
    payload = dict(
    password="123456@As",
    password2="123456@As"
    )

    response = customer_login_client.post(url, payload)

    assert response.data == {'msg':'Password Changed Successfully'}
    assert response.status_code == 200

@pytest.mark.django_db
def test_change_customer_invalid_password(customer_login_client):
    url = reverse('change_password_customer')
    payload = dict(
    password="123456@As",
    password2="123456@A"
    )

    response = customer_login_client.post(url, payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_send_password_reset_email(customer_login_client):
    url = reverse('send-password-reset-email')
    payload = dict(
        email='28001398bhargav@gmail.com'
    )

    response = customer_login_client.post(url, payload)

    assert response.data == {'msg':'Password Reset link send. Please check your Email'}
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_reset_customer_password(customer_login_client):
#     url = reverse('reset-password', kwargs={'uid':'MTY', 'token':'b8rf2f-651bfeaa50d3a9fa34b04c1a9d8da062'})
#     payload = dict(
#     password="123456@As",
#     password2="123456@As"
#     )
#
#     response = customer_login_client.post(url, payload)
#
#     # assert response.data == {'msg': 'Password Reset Successfully'}
#     # assert response.status_code == 200


@pytest.mark.django_db
def test_register_brand(client):
    payload = dict(
        username="zudio_brand",
        email= "zudio@gmail.com",
        password= "123456@As",
        password2= "123456@As",
        brand_name= "Zudio"
    )

    url = reverse('register_brand')
    response = client.post(url, payload)

    assert response.status_code == 201
    assert response.data['msg'] == 'Registration Has Been Done Sucessfully !'


@pytest.mark.django_db
def test_register_brand_fail(client):
    payload = dict(
        username="zudio_brand",
        email= "zudio@gmail.com",
        password= "123456@As",
        password2= "123456@As",
        brand_name= "zudio"
    )

    payload1 = dict(
        username="zudio_brand1",
        email="zudio@gmail1.com",
        password="123456@As",
        password2="123456@As",
        brand_name="zudio"
    )

    url = reverse('register_brand')
    client.post(url, payload)
    response = client.post(url, payload1)

    assert response.status_code == 409


@pytest.mark.django_db
def test_login_brand(brand, client):
    payload = dict(
        email=brand.email,
        password='123456@As',
    )

    url = reverse('login_brand')
    response = client.post(url, payload)

    assert response.data['msg'] == 'Login Success'
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_brand_fail(brand, client):
    payload = dict(
        email=brand.email,
        password='123456@A',
    )

    url = reverse('login_brand')
    response = client.post(url, payload)

    assert response.data == {'errors': {'non_field_errors':['Email or Password is not Valid']}}
    assert response.status_code == 404



@pytest.mark.django_db
def test_view_brand_profile(brand_login_client):
    url = reverse('profile_brand')
    response = brand_login_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_brand_profile(brand_login_client):

    payload = dict(
        email= "zudio@gmail.com",
        username= "zudio_brand",
        brand_name= "Zudio"
    )

    url = reverse('profile_brand')
    response = brand_login_client.put(url, payload)
    assert response.status_code == 200
    assert response.data == {'msg': 'Profile Updated Successfully'}


@pytest.mark.django_db
def test_delete_brand_profile(brand_login_client):
    url = reverse('profile_brand')
    response = brand_login_client.delete(url)
    assert response.status_code == 200
    assert response.data == {"message": "Brand deleted Successfully"}