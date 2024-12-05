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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "usertype",
            "dateJoined"
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
