from rest_framework import serializers
from django.http import JsonResponse
from .models import *
import logging

logger = logging.getLogger(__name__)

class UsertypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usertype
        fields = [
            "name"
        ]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "user",
            "followers",
            "fname",
            "mname",
            "lname",
            "suffix",
            "contact_num",
            "birthdate",
            "profile_img",
        ]
        
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "usertype",
            "dateJoined",
            "profile",
        ]
        
    def create(self, validated_data):
        # If profile data is provided, extract it and create a profile
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create(**validated_data)
        
        if profile_data:
            Profile.objects.create(user=user, **profile_data)  # Create profile for the user
        
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance = super().update(instance, validated_data)  # Update the user
        
        if profile_data:
            # If a profile already exists, update it
            profile_instance = instance.profile
            for attr, value in profile_data.items():
                setattr(profile_instance, attr, value)
            profile_instance.save()
        
        return instance

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "user",
            "photo",
            "caption",
            "likes",
            "createdAt"
        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "user",
            "post",
            "content",
            "likes",
            "createdAt",
            "reply"
        ]

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            "user",
            "submission",
            "caption",
            "likes",
            "createdAt"
        ]

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = [
            "submission",
            "score"
        ]

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = [
            "name"
        ]

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = [
            "name"
        ]

class EventSerializer(serializers.ModelSerializer):
    host = serializers.SerializerMethodField()
    judges = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "host",
            "judges",
            "competitors",
            "submissions",
            "eventType",
            "eventCategory",
            "name",
            "startDate",
            "endDate",
            "theme",
            "description",
            "submission_rules",
            "voting_criteria",
            "prizes",
            "event_banner",
            "createdAt"
        ]

    def get_host(self, obj):
        host_user = UserSerializer(obj.host)
        return obj.host.username
    
    def get_judges (self, obj):
        data = []

        for judge in obj.judges.all():
            temp = {judge.username}
            data.append(temp)

        return data
