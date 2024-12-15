from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage import default_storage
from .models import User

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
    
class UserDetails(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
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
#             logger.error(f"User not found: {data['username']}")
#             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

#         if check_password(data['password'], user.password):
#             try:
#                 Token.objects.filter(user=user).delete()  
#                 token, created = Token.objects.get_or_create(user=user) 

#                 logger.info(f"Token created for {user.username}: {created}, Token: {token.key}")

#                 return Response(
#                     {
#                         "success": True,
#                         "token": token.key, 
#                         "username": user.username,
#                     },
#                     status=status.HTTP_200_OK,
#                 )
#             except Exception as e:
#                 logger.error(f"Error creating token for {user.username}: {e}")
#                 return Response({"error": "Token creation failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             logger.error(f"Invalid credentials for user: {data['username']}")
#             return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

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

class PostUpload(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  
        data = request.data
        file = request.FILES.get("post")

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
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PostDisplay(APIView):
    def get(self, request):
        queryset = Post.objects.all().order_by('-createdAt')
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
        })
