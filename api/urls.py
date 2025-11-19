from django.urls import path

from .views import *

urlpatterns = [
    path('channels/',ChannelListAPIView.as_view()),
    path('channels/<str:pk>',ChannelDetailAPIView.as_view(), name='channel_details'),
    path('join-channel/',JoinChannelAPIView.as_view()),
]