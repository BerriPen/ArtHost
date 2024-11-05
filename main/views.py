from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
#import requests
from .models import *
from django.core import serializers
from .serializers import *

class EventList(APIView):
    def get(self, request):
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
