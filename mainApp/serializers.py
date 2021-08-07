from django.core.validators import validate_email
from django.db.models import fields
from django.utils.encoding import force_bytes
from  rest_framework import serializers, exceptions
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .models import User
from mainApp import models
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import DjangoUnicodeDecodeError,  force_str, smart_str, smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class RegistrasionSerialier(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 18 , min_length = 8 , write_only = True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('the username should contains Chars as well')

        return attrs

    def created(self, validated_data):
        return User.objects.create_user(**validated_data)

    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length = 300)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 18 , min_length = 8 , read_only = True)
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 18 , min_length = 8, write_only = True )
    tokens = serializers.CharField(max_length = 300, read_only = True)

    class Meta: 
        model = User
        fields = ['username','email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = authenticate(email=email, password=password)
        print(user)

        if not user :
            raise exceptions.AuthenticationFailed('there is no such user')

        if not user.is_active :
            raise exceptions.AuthenticationFailed('this user is not active contact the admin')

        if not user.is_verified :
            raise exceptions.AuthenticationFailed('this user account is not verified')

        return {
            'email':user.email,
            'username':user.username,
            'tokens':user.tokens()
        }

class RequestNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email',]


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 18 , min_length = 8, write_only = True )
    token = serializers.CharField(min_length = 1, write_only = True)
    uidb64 = serializers.CharField(min_length = 1, write_only = True)

    class Meta:
        fields = ['password','token','uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user_qs = User.objects.filter(id=id)
            if user_qs.exists():
                user = user_qs[0]
                valid_token = PasswordResetTokenGenerator().check_token(user, token)
                if not valid_token:
                    raise AuthenticationFailed('this token is invalid')

                user.set_password(password)
                user.save()
                return super().validate(attrs)

            raise exceptions.ValidationError('user not exists')
            
        except Exception as e:
            raise AuthenticationFailed('this token is invalid')
