from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password

#import requests
from .models import *
from django.core import serializers
from .serializers import *
import logging

logger = logging.getLogger(__name__)

class EventList(APIView):
    # serializer_class = EventSerializer

    def get(self, request):
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserList(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SignUp (APIView):
    def post(self, request):
        logger.info(request.data)
        data = request.data

        password = make_password(data['password'])
        info = {
            'username': data['username'],
            'email': data['email'],
            'password': password
        }
        serializer = UserSerializer(data=info)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({ "success": True }, status=status.HTTP_200_OK)

# class Login (APIView):
#     def post(self, request):
#         data = request.data
        
#         user = User.objects.get(username=data['username'])
#         logger.info(user.password)

#         logger.info(f"CHECKING PASSWORD: {check_password(data['password'], user.password)}")

#         if check_password(data['password'], user.password):
#             return True
#         return Response({ "success": True }, status=status.HTTP_200_OK)

class Login(APIView):
    def post(self, request):
        data = request.data

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if check_password(data['password'], user.password):
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        