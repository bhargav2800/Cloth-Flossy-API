from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, LoginUserSerializer, ProfileCustomerSerializer, ChangePasswordCustomerSerializer, SendPasswordResetEmailSerializer, PasswordResetCustomerSerializer, ProfileUserSerializer, RegisterBrandSerializer, ProfileBrandSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import User, Customer, Brand


# Generating Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class RegisterCustomer(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = RegisterUserSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     user = serializer.save()
        #     token = get_tokens_for_user(user)
        #     return Response({'token':token, 'msg': 'Registration Has Been Done Sucessfully !'}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Customer.objects.create(user=user,email=user.email)
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg': 'Registration Has Been Done Sucessfully !'}, status=status.HTTP_201_CREATED)


class LoginCustomer(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            # raise ValidationError({'errors': {'non_field_errors':['Email or Password is not Valid']}})
            return Response({'errors': {'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileCustomer(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = ProfileUserSerializer(request.user)
        serializer1 = ProfileCustomerSerializer(Customer.objects.get(user=request.user))
        return Response({"User":serializer.data, "Customer":serializer1.data}, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        serializer = ProfileUserSerializer(request.user, data=request.data)
        serializer1 = ProfileCustomerSerializer(Customer.objects.get(user=request.user), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer1.is_valid(raise_exception=True)
        serializer.save()
        serializer1.save()
        return Response({'msg': 'Profile Updated Successfully'}, status=status.HTTP_200_OK)


    def delete(self, request, format=None):
        user = self.request.user
        user.delete()
        return Response({"message": "user delete Successfully"}, status=status.HTTP_200_OK)

class ChangePasswordCustomer(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = ChangePasswordCustomerSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailCustomer(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetCustomer(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, uid, token, format=None):
        serializer = PasswordResetCustomerSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Seller

class RegisterBrand(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = RegisterUserSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     user = serializer.save()
        #     token = get_tokens_for_user(user)
        #     return Response({'token':token, 'msg': 'Registration Has Been Done Sucessfully !'}, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer1 = RegisterBrandSerializer(data={'user':user.id,'brand_name':request.data['brand_name'],'email':user.email})
        if serializer1.is_valid():
            customer = serializer1.save()
            user.is_staff = True
            token = get_tokens_for_user(user)
            user.save()
            return Response({'token':token, 'msg': 'Registration Has Been Done Sucessfully !'}, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(serializer1.errors,status=status.HTTP_409_CONFLICT)



class LoginBrand(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            # raise ValidationError({'errors': {'non_field_errors':['Email or Password is not Valid']}})
            return Response({'errors': {'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class ProfileBrand(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, format=None):
        serializer = ProfileUserSerializer(request.user)
        serializer1 = ProfileBrandSerializer(Brand.objects.get(user=request.user))
        return Response({"User":serializer.data, "Brand":serializer1.data}, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        serializer = ProfileUserSerializer(request.user, data=request.data)
        serializer1 = ProfileBrandSerializer(Brand.objects.get(user=request.user),data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer1.is_valid(raise_exception=True)
        serializer.save()
        serializer1.save()
        return Response({'msg': 'Profile Updated Successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        user = self.request.user
        user.delete()
        return Response({"message": "Brand deleted Successfully"}, status=status.HTTP_200_OK)
