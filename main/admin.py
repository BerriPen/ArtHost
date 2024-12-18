from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Usertype)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Comment)  
admin.site.register(Post)
admin.site.register(Submission)
admin.site.register(Evaluation)
admin.site.register(EventType)
admin.site.register(EventCategory)
admin.site.register(Event)

class UsertypeAdmin(admin.ModelAdmin):
    usertype = [
        "name"
    ]

class UserAdmin(admin.ModelAdmin):
    user = [
        "username",
        "email",
        "password",
        "usertype",
        "token",
        "dateJoined"
    ]

class ProfileAdmin(admin.ModelAdmin):
    profile = [
        "user",
        "followers",
        "bio",
        "fname",
        "mname",
        "lname",
        "suffix",
        "contact_num",
        "birthdate",
        "profile_img",
    ]

class PostAdmin(admin.ModelAdmin):
    post = [
        "user",
        "photo",
        "caption",
        "likes",
        "createdAt"
    ]

class CommentAdmin(admin.ModelAdmin):
    comment = [
        "user",
        "post",
        "content",
        "likes",
        "createdAt",
        "reply"
    ]

class SubmissionAdmin(admin.ModelAdmin):
    submission = [
        "user",
        "submission",
        "caption",
        "likes",
        "createdAt"
    ]

class EvaluationAdmin(admin.ModelAdmin):
    evaluation = [
        "submission",
        "score"
    ]

class EventTypeAdmin(admin.ModelAdmin):
    eventType = [
        "name"
    ]    

class EventCategoryAdmin(admin.ModelAdmin):
    eventCategory = [
        "name"
    ]

class EventAdmin(admin.ModelAdmin):
    event = [
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