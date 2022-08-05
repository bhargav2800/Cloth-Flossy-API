import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from customer.serializers import InvoiceSerializer
from .serializers import ProductsSerializer, ProductReviewsSerializer, UpdateInvoiceStatusSerializer, UpdateReturnOrderStatusSerializer, ReturnProductSerializer, ReplaceProductSerializer, UpdateReplaceOrderStatusSerializer
from rest_framework import viewsets, mixins
from .models import Product,Brand
from customer.models import Reviews, Invoice, ReturnProducts, ReplaceProducts

class ViewAllProducts(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        # print(request.kwargs)3
        products = Product.objects.filter(brand__user=self.request.user)
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductUpdateDeleteViewCreate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get_product_object(self, id):
        try:
            return Product.objects.get(id=id, brand__user=self.request.user)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, **kwargs):
        product = self.get_product_object(request.data['id'])
        if isinstance(product, Response):
            return Response({'msg':'Product Does Not Exist !'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(brand=Brand.objects.get(user=self.request.user))
        return Response({'msg':'Product Created Successfully'}, status=status.HTTP_200_OK)

    def put(self, request):
        product = self.get_product_object(request.data['id'])
        if isinstance(product, Response):
            return Response({'msg':'Product Does Not Exist !'},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductsSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Product Updated Successfully'}, status=status.HTTP_200_OK)

    def delete(self, request):
        product = self.get_product_object(request.data['id'])
        if isinstance(product, Response):
            return Response({'msg':'Product Does Not Exist !'},status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({'msg':'Product Deleted Successfully'}, status=status.HTTP_200_OK)


class ViewProductReviews(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, id):
        products_reviews = Reviews.objects.filter(product__brand__user=self.request.user, product__id=id)
        serializer = ProductReviewsSerializer(products_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewOrders(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        invoices = Invoice.objects.filter(product__brand__user = request.user)
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, id):
        try:
            invoice = Invoice.objects.get(id=id, product__brand__user=request.user)
        except Invoice.DoesNotExist:
            return Response({'msg': 'Invoice Order Does Not Exist !'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateInvoiceStatusSerializer(invoice,data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['status'] == 'Canceled' or serializer.validated_data['status'] == 'Returned' or serializer.validated_data['status'] == 'Replaced':
            return Response({'msg':'You are not allow to perform this operation'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.validated_data['status'] == 'Delivered':
                serializer.save(order_delivery_date=datetime.datetime.now())
            else:
                serializer.save()
            return Response({'msg':'Order Status Has Been Updated Successfully'}, status=status.HTTP_200_OK)




class ReturnOrders(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        invoices = ReturnProducts.objects.filter(invoice__product__brand__user=request.user)
        serializer = ReturnProductSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, id):
        try:
            return_product = ReturnProducts.objects.get(id=id, invoice__product__brand__user=request.user)
        except ReturnProducts.DoesNotExist:
            return Response({'msg': 'Return Order Does Not Exist !'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateReturnOrderStatusSerializer(return_product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Returned Product Order Status Has Been Updated Successfully'}, status=status.HTTP_200_OK)


class ReplaceOrders(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        invoices = ReplaceProducts.objects.filter(invoice__product__brand__user=request.user)
        serializer = ReplaceProductSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            replace_product = ReplaceProducts.objects.get(id=id, invoice__product__brand__user=request.user)
        except ReplaceProducts.DoesNotExist:
            return Response({'msg': 'Replace Product Order Does Not Exist !'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateReplaceOrderStatusSerializer(replace_product, data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['replace_delivery_status'] == 'Delivered':
            serializer.save(replace_delivery_date=datetime.datetime.now())
        else:
            serializer.save()
        return Response({'msg':'Replaced Product Order Status Has Been Updated Successfully'}, status=status.HTTP_200_OK)
