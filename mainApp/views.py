from re import I, S
from django.http import request
from django.shortcuts import render
from rest_framework import generics, serializers, status, views
from .serializers import (
    RegistrasionSerialier, 
    EmailVerificationSerializer, 
    LoginSerializer, 
    RequestNewPasswordSerializer,
    ResetPasswordSerializer,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Utils
from rest_framework.decorators import api_view
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .renderers import UserRenserer
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import DjangoUnicodeDecodeError,  force_str, smart_str, smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Utils

class RegisterView(generics.GenericAPIView):

    serializer_class = RegistrasionSerialier
    renderer_classes = (UserRenserer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        data = serializer.data
        user = User.objects.get(email=data['email'])

        # create the link that will allow the user to activite his account and which includ toekn
        token = RefreshToken.for_user(user).access_token #for_user is a built in function
        current_site_domain = get_current_site(request).domain
        relative_link = reverse('verify_email')
        absurl = f'http://{current_site_domain}{relative_link}?token={token}'

        email_body = f'Hi dear thanks for your registration /n can you please verfy your account trough this link /n {absurl} ... thank you'
        data = {
            'subject':'Verify your account',
            'body':email_body,
            'to_email':user.email
        }
        Utils.send_email(data)


        return Response(data, status=status.HTTP_201_CREATED)


class VerifyEmailView(views.APIView):

    serializer_class = EmailVerificationSerializer
    # this is just to allow or add token field in the api documentation
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='description', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        # get the token from the request
        token = request.GET.get('token')
        try:

            # decoding the token and while doing that it use the app secret key
            payload = jwt.decode(token, settings.SECRET_KEY) # decode is a built in func and secret key is from settings.py
            user_id = payload['user_id'] # we get the user id from the token so we can verify 
            
            user = User.objects.get(id=user_id)
            user.is_verified = True
            user.save()


            return Response({'email':'activated sucessfuly'}, status=status.HTTP_201_CREATED)

        except jwt.ExpiredSignatureError as identifier :
            return Response({'error':'the link is expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier :
            return Response({'error':'invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)



class RequestNewPasswordAPIView(generics.GenericAPIView):

    serializer_class = RequestNewPasswordSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        user_qs = User.objects.filter(email=request.data['email'])
        if user_qs.exists():
            user = user_qs[0]
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site_domain = get_current_site(request).domain
            relative_link = reverse('verify_token', kwargs={'uidb64':uidb64, 'token':token})
            absurl = f'http://{current_site_domain}{relative_link}'
            email_body = f'Hi dear thanks for your request \n this is ur resetting pasword link: \n {absurl}'
            data = {
                'subject':'Reset your password',
                'body':email_body,
                'to_email':user.email
            }
            Utils.send_email(data)

            return Response({'success':'the reset link has been succesfully sent to ur email'},status=status.HTTP_200_OK)
        
        return Response({'Error':'This user is not exisrs'},status=status.HTTP_404_NOT_FOUND)



class VerifyResetPasswordTokenAPIView(generics.GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user_qs = User.objects.filter(id=id)
            if user_qs.exists():
                user = user_qs[0]
                token = PasswordResetTokenGenerator().check_token(user, token)
                if not token:
                    return Response({'Error':'this token is invalid'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'Success':'everything is valid'}, status=status.HTTP_200_OK)
            return Response({'Error':'user is not exists'}, status=status.HTTP_400_BAD_REQUEST)

        except DjangoUnicodeDecodeError as e:
            return Response({'Error':'fail at decoding the information'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({'success':True,'message':'password has sucessfuly reset'}, status=status.HTTP_200_OK)