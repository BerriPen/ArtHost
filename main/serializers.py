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
    user = serializers.CharField(source="user.username")
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
        profile = Profile.objects.filter(user=obj.user).first()
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
    host = serializers.CharField(source="host.username", read_only=True)
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
            "createdAt",
        ]
        read_only_fields = ["createdAt"]

    def get_judges(self, obj):
        return [judge.username for judge in obj.judges.all()]

    def validate(self, data):
        if data['startDate'] >= data['endDate']:
            raise serializers.ValidationError("Start date must be earlier than end date.")
        return data
