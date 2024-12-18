from rest_framework import routers
from django.urls import re_path
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

router = routers.DefaultRouter()

urlpatterns = router.urls + [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

    re_path('eventList', EventList.as_view(), name="event-list"),
    re_path('eventDetails/<int:id>', EventDetails.as_view(), name='event-details'),
    # re_path('userList', UserList.as_view(), name="user-list"), 
    re_path('userDetails', UserDetails.as_view(), name='user-details'),
    # re_path('userProfile', UserProfile.as_view(), name='user-profile'),
    re_path('signup', SignUp.as_view(), name='user-signup'),

    re_path('login', Login.as_view(), name='user-login'),
    re_path('logout', Logout.as_view(), name='user-logout'),

    re_path('postDisplay', PostDisplay.as_view(), name='post-display'),
    re_path('postUpload', PostUpload.as_view(), name='post-upload'),
    re_path('createEvent', CreateEvent.as_view(), name='create-event'),
]

