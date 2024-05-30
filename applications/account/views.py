import logging
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model 
# from rest_framework.viewsets import generics 
from core.account import generics
from applications.account.serializers import (
    RegisterSerializer, ChangePasswordSerializer, 
    ForgotPasswordSerializer, ForgotPasswordConfirmSerializer,
    ProfileSerializer, ChangeProfileSerializer
)
from applications.feedback.views import FeedbackMixin

from drf_yasg.utils import swagger_auto_schema

User = get_user_model()
logger = logging.getLogger("main")


class ProfileListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    
    
class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer


class ChangeProfileAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangeProfileSerializer
    permission_classes = [IsAuthenticated]


class RegisterAPIView(APIView):

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("User registered.")
        return Response("You have successfully registred. "
                        "We sent an activation email",
                        status=status.HTTP_201_CREATED)
    
    
class ActivationAPIView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ""
            user.save()
            logger.info("User activated account.")
            return Response({"message": "successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.info("Something get wrong in account activation.")
            return Response({"message": "Wrong email!"}, status=status.HTTP_400_BAD_REQUEST)
        
    
class ChangePasswordAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        logger.info("User changed password.")
        return Response("Password updated successfully...")
    
    
class ForgotPasswordAPIView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        logger.info("User has requested new password.")
        return Response("We sent code to reset your password.")
    

class ForgotPasswordConfirmAPIView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordConfirmSerializer)
    def post(self, request):
        serializer = ForgotPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        logger.info("User changed password.")
        return Response("Password updated successfully.")