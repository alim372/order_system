from django.shortcuts import render
from rest_framework.parsers import  MultiPartParser, FormParser, JSONParser
from rest_framework import viewsets
from rest_framework.decorators import parser_classes, api_view, permission_classes, authentication_classes, action
from django.db import IntegrityError, transaction
from django.conf import settings
# login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
# api response 
from rest_framework.response import Response
from order_system_paymob_accept.api_response import prepare_response
# serializers
from .serializers import UserSerializer, ChangePasswordSerializer
# models
from .models import User, StatusChoices
# authorization
from order_system_paymob_accept.middleware.authorization import administrator, user 
# Authentication
from order_system_paymob_accept.middleware.authentication import ExpiringTokenAuthentication
# validation 
from .minlengthpass import MinimumLengthValidator
# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from order_system_paymob_accept.swagger_responce_schema import *

class Auth(ObtainAuthToken, viewsets.ModelViewSet):
    parser_classes = [JSONParser]
    @swagger_auto_schema(
        tags=(['Auth']),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'password': openapi.Schema(format=openapi.FORMAT_PASSWORD, type=openapi.TYPE_STRING, description='string'),
            }
        ))
    @action(detail=True, methods=['POST'])
    def login(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.filter(user=user).first()
        if token:
            token.delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response(prepare_response({}, {
                    'token': token.key,
                    'user': UserSerializer(user).data
                }), 201)

    @swagger_auto_schema(
        tags=(['Auth']),
        request_body=UserSerializer,
        responses=createResponseSchema(UserSerializer)
    )
    @action(detail=True, methods=['POST'])
    @transaction.atomic
    def signup(self, request):
        """
         new users signup.
        """
        user = User()
        # create all from post
        for attr, value in request.data.items():
            # if field is allowed
            if attr not in User.protected():
                setattr(user, attr, value)
        try:
            with transaction.atomic():
                # set password
                if 'password' in request.data :
                    MinimumLengthValidator().validate(request.data['password'])
                    user.set_password(request.data['password'])
                # save data
                user.save()
                # GET new data
                serializer = UserSerializer(user, many=False)
                # retuen new data
                token, created = Token.objects.get_or_create(user=user)
                return Response(prepare_response({}, {
                    'token': token.key,
                    'user':serializer.data
                }), 201)
        except Exception as error:
            # return valiation error
            return Response(prepare_response({"status": 422, "instance": request.get_full_path()}, error, False), 422)


class Profile(viewsets.ModelViewSet):
    authentication_classes = [ExpiringTokenAuthentication]
    @swagger_auto_schema(
        tags=(['Profile']),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(format=openapi.FORMAT_PASSWORD, type=openapi.TYPE_STRING, description='string'),
                'new_password': openapi.Schema(format=openapi.FORMAT_PASSWORD, type=openapi.TYPE_STRING, description='string'),
            }
        ))
    @action(detail=True, methods=['POST'])
    def changePassword(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not request.user.check_password(old_password):
                return Response(prepare_response({"status": 422, "instance": "logs/error"}, [["old_password", ["Wrong password."]]], False), 422)

            # set_password also hashes the password that the user will get
            request.user.set_password(serializer.data.get("new_password"))
            request.user.save()
            return Response(prepare_response({"message": 'Your password was successfully updated!'}, {}), 201)

        return Response(prepare_response({"status": 422, "instance": "logs/error"}, [["new_password", ['The password does not meet the password policy requirements']]], False), 422)

    @swagger_auto_schema(
        tags=(['Profile']),
        responses=recordResponseSchema(UserSerializer)
    )
    @action(detail=True, methods=['GET'])
    def logout(self, request):
        """
        GET user by id .
        """
        token = Token.objects.filter(user=request.user).first()
        if token != None:
            token.delete()
        return Response(prepare_response({}, {}))

