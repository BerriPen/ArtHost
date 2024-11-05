from rest_framework import routers
from django.urls import re_path

from .views import *

router = routers.DefaultRouter()

urlpatterns = router.urls + [
    re_path('eventList', EventList.as_view(), name="event-list"),
]