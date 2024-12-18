from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .models import Event, Post
from .serializers import *
import logging

logger = logging.getLogger(__name__)

# Utility Functions
def success_response(data=None, message="Success"):
    return Response({"success": True, "message": message, "data": data}, status=status.HTTP_200_OK)

def error_response(errors=None, message="Error", code=status.HTTP_400_BAD_REQUEST):
    return Response({"success": False, "message": message, "errors": errors}, status=code)

# Event Views
class EventList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return success_response(data=serializer.data)

class EventDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        try:
            event = Event.objects.get(id=id)
            serializer = EventSerializer(event)
            return success_response(data=serializer.data)
        except Event.DoesNotExist:
            return error_response(message="Event not found", code=status.HTTP_404_NOT_FOUND)

class CreateEvent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Event created: {serializer.data}")
            return success_response(data=serializer.data, message="Event created successfully")
        return error_response(errors=serializer.errors, message="Event creation failed")

# User Views
class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if User.objects.filter(email=data.get('email')).exists():
            return error_response(message="Email is already in use")

        data['password'] = make_password(data.get('password'))
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="User registered successfully")
        return error_response(errors=serializer.errors, message="Registration failed")

class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return success_response(data={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, message="Login successful")
        return error_response(message="Invalid credentials", code=status.HTTP_401_UNAUTHORIZED)

class UserDetails(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        return success_response(data={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "profile_img": user.profile.profile_img.url if hasattr(user, 'profile') and user.profile.profile_img else None,
        }, message="User details fetched successfully")

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = request.headers.get('Authorization').split()[1]
            outstanding_token = OutstandingToken.objects.get(token=token)
            BlacklistedToken.objects.create(token=outstanding_token)
            return success_response(message="Logged out successfully")
        except Exception as e:
            return error_response(message="Error logging out", errors=str(e))

# Post Views
class PostUpload(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        file = request.FILES.get("post")

        if not file:
            return error_response(message="File is required")

        info = {
            "caption": data.get("caption", ""),
            "post": file,
            "user": request.user,
        }

        serializer = PostSerializer(data=info)
        if serializer.is_valid():
            serializer.save()
            return success_response(data=serializer.data, message="Post uploaded successfully")
        return error_response(errors=serializer.errors, message="Post upload failed")

class PostDisplay(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        posts = Post.objects.all().order_by('-createdAt')
        serializer = PostSerializer(posts, many=True)
        return success_response(data=serializer.data, message="Posts fetched successfully")

# Secure Data Example
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def secure_data(request):
    return success_response(message="This is protected data!")
