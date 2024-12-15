from rest_framework import serializers
from django.http import JsonResponse
from .models import *
import logging

from main.models import User

logger = logging.getLogger(__name__)


class UsertypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usertype
        fields = [
            "name"
        ]

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "usertype",
            "dateJoined"
        ]

# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = Profile
#         fields = [
#             "user",
#             "followers",
#             "fname",
#             "mname",
#             "lname",
#             "suffix",
#             "contact_num",
#             "birthdate",
#             "profile_img",
#         ]

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    
    # Check if the user is authenticated and has a profile
    fname = serializers.CharField(source="fname", required=False)
    mname = serializers.CharField(source="mname", required=False)
    lname = serializers.CharField(source="lname", required=False)
    suffix = serializers.CharField(source="suffix", required=False)
    contact_num = serializers.CharField(source="contact_num", required=False)
    birthdate = serializers.DateField(source="birthdate", required=False)
    profile_img = serializers.ImageField(source="profile_img", required=False)

    class Meta:
        model = Profile
        fields = [
            "user",
            "fname",
            "mname",
            "lname",
            "suffix",
            "contact_num",
            "birthdate",
            "profile_img",
        ]
    
    def to_representation(self, instance):
        # Ensure that only authenticated users can access profile details
        if not self.context['request'].user.is_authenticated:
            return {}  # Return an empty dictionary or handle as needed
        return super().to_representation(instance)

class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "user",
            "photo",
            "caption",
            "likes",
            "createdAt",
            "avatar",
        ]

    def get_avatar(self, obj):
        profile = getattr(obj.user, 'profile', None)
        if profile and profile.profile_img:
            return profile.profile_img.url
        return 'https://cdn.quasar.dev/img/boy-avatar.png' 

class CommentSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source="likes.count", read_only=True)

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

# class EventSerializer(serializers.ModelSerializer):
#     host = serializers.SerializerMethodField()
#     judges = serializers.SerializerMethodField()

#     class Meta:
#         model = Event
#         fields = [
#             "host",
#             "judges",
#             "competitors",
#             "submissions",
#             "eventType",
#             "eventCategory",
#             "name",
#             "startDate",
#             "endDate",
#             "theme",
#             "description",
#             "submission_rules",
#             "voting_criteria",
#             "prizes",
#             "event_banner",
#             "createdAt"
#         ]

#     def get_host(self, obj):
#         host_user = UserSerializer(obj.host)
#         return obj.host.username
    
#     def get_judges (self, obj):
#         return [judge.username for judge in obj.judges.all()]
    
#     def validate(self, data):
#         if data['startDate'] >= data['endDate']:
#             raise serializers.ValidationError("Start date must be earlier than end date.")
#         return data

class EventSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    judges = UserSerializer(many=True, read_only=True)

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
            "createdAt",
        ]
        read_only_fields = ["createdAt"]

    def validate(self, data):
        if data['startDate'] >= data['endDate']:
            raise serializers.ValidationError("Start date must be earlier than end date.")
        return data