import datetime
import json
import os
import razorpay as razorpay
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins
from seller.models import Product, Brand
from account.models import Customer
from .models import Cart, WishList, Reviews, Favourites, Order, Invoice, ReturnProducts, ReplaceProducts
from .serializers import ViewProductSerializer, CartSerializer, WishListSerializer, ProductReviewSerializer, FavouriteBrandSerializer, OrderSerializer, OrderAddressSerializer, InvoiceSerializer, ReturnProductSerializer, ReplaceProductSerializer, ReturnReasonSerializer, ReplaceReasonSerializer
from django.http import HttpResponse
import webbrowser


class ViewAllProducts(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.all()
        serializer = ViewProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewProductDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_product_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        product = self.get_product_object(id)
        if isinstance(product, Response):
            return Response({'msg': 'Product Does Not Exist !'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ViewProductSerializer(product)
        return Response(serializer.data)


class ViewSearchedProduct(APIView):
    def get(self, request, search_value):
        q = search_value
        product = Product.objects.filter(
            Q(name__icontains=q) | Q(short_line__icontains=q) | Q(brand__brand_name__icontains=q) | Q(
                category__name__icontains=q))
        serializer = ViewProductSerializer(product, many=True)
        return Response(serializer.data)


class ViewTrendingProduct(APIView):
    def get(self, request):
        product = Product.objects.order_by('no_of_purchases')[:10]
        serializer = ViewProductSerializer(product, many=True)
        return Response(serializer.data)


class CartAddRemoveUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart_product_object(self, id):
        try:
            return Cart.objects.get(product__id=id, customer__user=self.request.user)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        cart_products = Cart.objects.filter(customer__user=self.request.user)
        serializer = CartSerializer(cart_products, many=True)
        return Response(serializer.data)

    def post(self, request, id=None):
        if Cart.objects.filter(product__id=id, customer__user=self.request.user).exists():
            return Response({'msg': 'Product Already Exist in Your Cart'}, status=status.HTTP_409_CONFLICT)
        else:
            serializer = CartSerializer(data={'product': id}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(customer=Customer.objects.get(user=self.request.user))
            return Response({'msg': 'Product Added To Cart Successfully'}, status=status.HTTP_200_OK)

    def put(self, request, id=None):
        cart_product = self.get_cart_product_object(id)
        if isinstance(cart_product, Response):
            return Response({'msg': 'Product Does Not Exist In Your Cart!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart_product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['added_quantity'] > cart_product.product.quantity:
            return Response({'msg': 'Out Of Stock'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'msg': 'Product Quantity has been Updated Successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        cart_product = self.get_cart_product_object(id)
        if isinstance(cart_product, Response):
            return Response({'msg': 'Product Does Not Exist In Your Cart !'}, status=status.HTTP_404_NOT_FOUND)
        cart_product.delete()
        return Response({'msg': 'Product Has Been Removed From Cart Successfully'}, status=status.HTTP_200_OK)



class WishListAddRemoveUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_wishlist_product_object(self, id):
        try:
            return WishList.objects.get(product__id=id, customer__user=self.request.user)
        except WishList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        wishlist_products = WishList.objects.filter(customer__user=self.request.user)
        serializer = WishListSerializer(wishlist_products, many=True)
        return Response(serializer.data)


    def post(self, request, id=None):
        if WishList.objects.filter(product__id=id, customer__user=self.request.user).exists():
            return Response({'msg': 'Product Already Exist in Your WishList'}, status=status.HTTP_409_CONFLICT)
        else:
            serializer = WishListSerializer(data={'product': id}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(customer = Customer.objects.get(user=self.request.user))
            return Response({'msg': 'Product Added To Cart Successfully'}, status=status.HTTP_200_OK)


    def delete(self, request, id=None):
        wishlist_product = self.get_wishlist_product_object(id)
        if isinstance(wishlist_product, Response):
            return Response({'msg': 'Product Does Not Exist In Your WishList !'}, status=status.HTTP_404_NOT_FOUND)
        wishlist_product.delete()
        return Response({'msg': 'Product Has Been Removed From WishList Successfully'}, status=status.HTTP_200_OK)


class ProductReviewAddUpdateDelete(APIView):
    permission_classes = [IsAuthenticated]

    def get_product_review_object(self, id):
        try:
            return Reviews.objects.get(id=id, customer__user=self.request.user)
        except Reviews.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id=None):
        if Product.objects.filter(id=id).exists():
            serializer = ProductReviewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(customer=Customer.objects.get(user=self.request.user), product=Product.objects.get(id=id))
            return Response({'msg': 'Product Review Added has Been Added Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Product Does Not Exists'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id=None):
        product_review = self.get_product_review_object(id)
        if isinstance(product_review, Response):
            return Response({'msg': 'Product Review Does Not Exist !'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductReviewSerializer(product_review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Product Review Has been Updated Successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        product_review = self.get_product_review_object(id)
        if isinstance(product_review, Response):
            return Response({'msg': 'Product review Does Not Exist !'}, status=status.HTTP_404_NOT_FOUND)
        product_review.delete()
        return Response({'msg': 'Product Review Has Been Deleted Successfully'}, status=status.HTTP_200_OK)


class FavouriteBrands(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        if Favourites.objects.filter(brand__id=id).exists():
            return Response({'msg': 'Brand Already Exist In Favourite Section !'}, status=status.HTTP_409_CONFLICT)
        else:
            serializer = FavouriteBrandSerializer(data={'customer': Customer.objects.get(user=self.request.user).id,
                                                        'brand': Brand.objects.get(id=id).id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'msg': 'Brand has Been Added Successfully to favourite section'},
                            status=status.HTTP_200_OK)

    def delete(self, request, id=None):
        try:
            fav_instance = Favourites.objects.get(brand__id=id, customer__user=self.request.user)
            fav_instance.delete()
            return Response({'msg': 'Brand Has Been Removed Successfully From Fav Section'}, status=status.HTTP_200_OK)
        except Favourites.DoesNotExist:
            return Response({'msg': 'Brand Does Not Exists in Fav Section!'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id=None):
        fav_brands = Favourites.objects.filter(customer__user=self.request.user)
        serializer = FavouriteBrandSerializer(fav_brands, many=True)
        return Response(serializer.data)


class OrderBuyCartCod(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_products = Cart.objects.filter(customer__user=request.user)
        if len(cart_products) > 0:
            serializer = OrderAddressSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order_instance = serializer.save(customer=Customer.objects.get(user=request.user))
            total_amount_count = 0
            for i in cart_products:
                total_amount_count += i.get_total
                Invoice.objects.create(order=order_instance, product=i.product, product_quantity=i.added_quantity, brand_name=i.product.brand.brand_name, product_name=i.product.name, buy_price=i.product.discount_price(), product_discount=i.product.discount, product_size=i.product.size.size, product_color=i.product.color.colour)
                product_instance = Product.objects.get(id=i.product.id)
                product_instance.quantity -= i.added_quantity
                product_instance.save()

            order_instance.total_amount = total_amount_count
            order_instance.order_id = order_instance.order_date.strftime('PAY2ME%Y%m%dODR') + str(order_instance.id)
            order_instance.save()

            return Response({'msg': 'Your Order Has Been Submited Successfully'}, status=status.HTTP_200_OK)

        else:
            return Response({'msg': 'Your Cart Is Empty ! '}, status=status.HTTP_204_NO_CONTENT)


    def get(self, request):
        orders = Order.objects.filter(customer__user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


load_dotenv()
client = razorpay.Client(auth=(os.environ.get('RAZORPAY_API_KEY'), os.environ.get('RAZORPAY_API_SECRET_KEY')))

class OrderBuyCartRazorpay(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart_products = Cart.objects.filter(customer__user=request.user)
        if len(cart_products) > 0:
            serializer = OrderAddressSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            total_amount_count = 0
            for i in cart_products:
                total_amount_count += i.get_total


            order_amount = total_amount_count
            order_currency = 'INR'
            razorpay_order = client.order.create(dict(amount=order_amount * 100, currency=order_currency, payment_capture='0'))
            customer = Customer.objects.get(user=request.user)

            payment = client.payment_link.create({
                "amount": total_amount_count * 100,
                "currency": "INR",
                "description": f"{razorpay_order['id']}Transaction",
                "callback_url": 'http://' + str(get_current_site(request)) + '/customer/paymentHandler/',
                "reference_id": razorpay_order['id'],
                "customer": {
                    "name": f"{customer.name}",
                    "email": f"{customer.email}",
                    "contact": f"{customer.mobile_no}"
                },
                "notify": {
                    "sms": True,
                    "email": True
                },
                "reminder_enable": True,
                "notes": {
                    "order_address":serializer.data['address'],
                    "email": f"{customer.email}",
                    "razorpay_order_id": razorpay_order['id']
                },
            })




            return Response({'response': payment}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Your Cart Is Empty ! '}, status=status.HTTP_204_NO_CONTENT)



class PaymentHandler(APIView):
    def get(self, request):
        try:
            params_dict = {'payment_link_id': request.GET.get('razorpay_payment_link_id', ''),
                           'payment_link_reference_id': request.GET.get('razorpay_payment_link_reference_id', ''),
                           'payment_link_status': request.GET.get('razorpay_payment_link_status', ''),
                           'razorpay_payment_id': request.GET.get('razorpay_payment_id', ''),
                           'razorpay_signature': request.GET.get('razorpay_signature', '')
                           }
            try:
                order_db = Order.objects.get(razorpay_order_id=params_dict['payment_link_reference_id'])
            except:
                return HttpResponse("505 Not Found")
            order_db.razorpay_payment_id = params_dict['razorpay_payment_id']
            order_db.razorpay_signature = params_dict['razorpay_signature']
            order_db.save()
            result = client.utility.verify_payment_link_signature(params_dict)
            if result:
                order_db.payment_status = 'SUCCESS'
                order_db.save()
                for product in Invoice.objects.filter(order=order_db):
                    product_instance = Product.objects.get(id=product.product.id)
                    product_instance.quantity -= product.product_quantity
                    product_instance.save()
                return HttpResponse("Payment Done Successfully")
            else:
                order_db.payment_status = 'FAILURE'
                order_db.save()
                return HttpResponse("Payment Has Been Fail")
        except:
            return HttpResponse("505 not found")


    def post(self, request):
        captured_data = json.loads(request.body)
        captured_header = request.headers
        try:
            client.utility.verify_webhook_signature(str(request.body, 'utf-8'),captured_header['X-Razorpay-Signature'], os.environ.get('RazorpayWebhookSecretKey'))
            if captured_data['event'] == 'payment.failed':
                email = captured_data['payload']['payment']['entity']['notes']['email']
                customer = Customer.objects.get(email=email)
                order = Order.objects.create(customer=customer,
                                             address=captured_data['payload']['payment']['entity']['notes']['order_address'],
                                             total_amount=captured_data['payload']['payment']['entity']['amount'] / 100,
                                             payment_method=f"RazorPay {captured_data['payload']['payment']['entity']['method']}",
                                             razorpay_order_id=captured_data['payload']['payment']['entity']['notes']['razorpay_order_id'],  payment_status='FAILURE', order_status="FAIL")
                order.order_id = order.order_date.strftime('PAY2ME%Y%m%dODR') + str(order.id)
                order.save()
                cart_products = Cart.objects.filter(customer=customer)
                for i in cart_products:
                    Invoice.objects.create(order=order, product=i.product, product_quantity=i.added_quantity,
                                           brand_name=i.product.brand.brand_name, product_name=i.product.name,
                                           buy_price=i.product.discount_price(), product_discount=i.product.discount,
                                           product_size=i.product.size.size, product_color=i.product.color.colour, status="Failed")
                return Response(status=status.HTTP_200_OK)
            else:
                email = captured_data['payload']['payment']['entity']['notes']['email']
                customer = Customer.objects.get(email=email)
                order = Order.objects.create(customer=customer, address=captured_data['payload']['payment']['entity']['notes']['order_address'], total_amount=captured_data['payload']['payment']['entity']['amount']/100, payment_method=f"RazorPay {captured_data['payload']['payment']['entity']['method']}", razorpay_order_id=captured_data['payload']['payment']['entity']['notes']['razorpay_order_id'])
                order.order_id = order.order_date.strftime('PAY2ME%Y%m%dODR') + str(order.id)
                order.save()
                cart_products = Cart.objects.filter(customer=customer)
                for i in cart_products:
                    Invoice.objects.create(order=order, product=i.product, product_quantity=i.added_quantity,
                                           brand_name=i.product.brand.brand_name, product_name=i.product.name,
                                           buy_price=i.product.discount_price(), product_discount=i.product.discount,
                                           product_size=i.product.size.size, product_color=i.product.color.colour)
                return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            order = Order.objects.get(id=id, customer__user=request.user)
        except Order.DoesNotExist:
            return Response({"msg":'Order Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

        invoices = Invoice.objects.filter(order=order)
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            order = Order.objects.get(id=id, customer__user=request.user)
        except Order.DoesNotExist:
            return Response({"msg": 'Order Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)

        Invoice.objects.filter(order=order).update(delivery_status='Canceled')
        order.order_status = 'CANCELED'
        order.save()
        return Response({'msg':'Order Has Been Cancled Successfullys'}, status=status.HTTP_200_OK)


class ReturnProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return_products = ReturnProducts.objects.filter(invoice__order__customer__user = request.user)
        serializer = ReturnProductSerializer(return_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        try:
            invoice = Invoice.objects.get(id=id, order__customer__user=request.user)
        except Invoice.DoesNotExist:
            return Response({"msg": 'Product Has Been Not Ordered By you'}, status=status.HTTP_404_NOT_FOUND)

        if invoice.status == 'Delivered':
            serializer = ReturnReasonSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            ReturnProducts.objects.create(invoice=invoice, returned_date=datetime.datetime.now(), returned_reason=serializer.data['returned_reason'])
            invoice.status = 'Returned'
            invoice.save()
            return Response({'msg':'Product Return Request Has Been Added Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'This Product is not elligible For Return'}, status=status.HTTP_400_BAD_REQUEST)


class ReplaceProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        replace_products = ReplaceProducts.objects.filter(invoice__order__customer__user = request.user)
        serializer = ReplaceProductSerializer(replace_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        try:
            invoice = Invoice.objects.get(id=id, order__customer__user=request.user)
        except Invoice.DoesNotExist:
            return Response({"msg": 'Product Has Been Not Ordered By you'}, status=status.HTTP_404_NOT_FOUND)

        if invoice.status == 'Delivered':
            serializer = ReplaceReasonSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(invoice=invoice, replaced_date= datetime.datetime.now())
            invoice.status = 'Replaced'
            invoice.save()
            return Response({'msg': 'Product Replace Request Has Been Added Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'This Product is not elligible For Replacement'}, status=status.HTTP_400_BAD_REQUEST)