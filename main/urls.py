from rest_framework import routers
from django.urls import re_path

from .views import *

router = routers.DefaultRouter()

urlpatterns = router.urls + [
    re_path('eventList', EventList.as_view(), name="event-list"),
    re_path('userList', UserList.as_view(), name="user-list"), 
    re_path('signup', SignUp.as_view(), name='user-signup'),
    re_path('login', Login.as_view(), name='user-login'),
    re_path('postDisplay', PostDisplay.as_view(), name='post-display'),
]