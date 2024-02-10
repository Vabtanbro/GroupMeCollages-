from django.urls import path
from .views import *



urlpatterns = [
    path('msg-in/', ProcessIncomingMsg.as_view()),
    path('msg-in/lostandfound/', LostAndFound.as_view()),
    path('msg-in-direct/', ProcessIncomingMsgDirect.as_view()),
]