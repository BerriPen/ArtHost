from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import default_storage
from .models import User

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

#import requests
from .models import *
from django.core import serializers
from .serializers import *
import logging

logger = logging.getLogger(__name__)

class EventList(APIView):
    def get(self, request):
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserList(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# class UserDetails(APIView):
#     def get(self, request):
#         user = request.user
#         serializer = ProfileSerializer(user)
#         return Response(serializer.data)

class UserDetails(APIView):
    permission_classes = [IsAuthenticated]  # Ensure this is added

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    
class SignUp (APIView):
    def post(self, request):
        logger.info(request.data)
        data = request.data

        if User.objects.filter(email=data['email']).exists():
            return Response({"error": "Email is already in use."}, status=status.HTTP_400_BAD_REQUEST)

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
    
class CreateEvent(APIView):
    def post(self, request):
        data = request.data

        info ={
            'eventName': data['name'],
            'eventTheme': data['theme'],
            'eventDesc': data['description'],
            'selectedJudges': data['judges'],
            'subRules': data['submission_rules'],
            'voteCriteria': data['voting_criteria'],
            'prizes': data['prizes'],
            'eventType': data['eventType'],
            'eventCat': data['eventCategory'],
            'startDate': data['startDate'],
            'endDate': data['endDate'],
        }
        serializer = EventSerializer(data=info)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({ "success": True }, status=status.HTTP_200_OK)

# class Login(APIView):
#     def post(self, request):
#         data = request.data

#         try:
#             user = User.objects.get(username=data['username'])
#         except User.DoesNotExist:
#             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

#         if check_password(data['password'], user.password):
#             return Response({"success": True}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self, request):
        data = request.data

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if check_password(data['password'], user.password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "success": True,
                "access_token": access_token,  
                "user": {"username": user.username, "email": user.email}
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

# class PostUpload(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user  
#         data = request.data
#         file = request.FILES.get("post")

#         if not file:
#             return Response({"error": "File is required"}, status=status.HTTP_400_BAD_REQUEST)

#         info = {
#             "caption": data.get("caption", ""),
#             "post": file,
#             "user": user,  
#         }

#         serializer = PostSerializer(data=info)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)

#         return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PostUpload(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  
        data = request.data
        file = request.FILES.get("post")

        logger.info(f"Received post upload request from user {user.username}")
        logger.info(f"Request data: {data}")
        
        if not file:
            return Response({"error": "File is required"}, status=status.HTTP_400_BAD_REQUEST)

        info = {
            "caption": data.get("caption", ""),
            "post": file,
            "user": user,  
        }

        serializer = PostSerializer(data=info)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Post uploaded successfully: {serializer.data}")
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)

        logger.error(f"Serializer errors: {serializer.errors}")
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PostDisplay(APIView):
    def get(self, request):
        queryset = Post.objects.all().order_by('-createdAt')
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
