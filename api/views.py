from django.shortcuts import render
from editor.models import Channel, UserProfile, CodeFile
from .serializers import ChannelSerializer,JoinChannelSerializer,ChannelDetailsSerializer
# Create your views here.
from rest_framework import generics,permissions
from rest_framework.response import Response
from django.db.models import Prefetch

# get object or get 404
from django.shortcuts import get_object_or_404

class ChannelListAPIView(generics.ListAPIView):
    serializer_class = ChannelSerializer
    permission_classes =[permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        user = self.request.user
        # Adjust depending on your model relationship
        return(
            Channel.objects.filter(participants__user=user)
            .select_related('created_by')
            .prefetch_related('participants')
        )
    
class JoinChannelAPIView(generics.GenericAPIView):
    serializer_class = JoinChannelSerializer
    permission_classes =[permissions.IsAuthenticated]
    
    def post(self, request):
        print(request.data)
        pk = request.data.get('channel_id')
        user = request.user
        try:
            channel = Channel.objects.get(pk=pk)
        except Channel.DoesNotExist:
            return Response({"detail": "Channel not found."}, status=404)
        
        if channel.participants.filter(user=user).exists():
            return Response({"detail": "User already in channel."}, status=400)
        
        user_profile = get_object_or_404(UserProfile, user=user)
        channel.participants.add(user_profile)
        channel.save()
        
        serializer = self.get_serializer(channel)
        return Response(serializer.data)
    
    def get(self, reqeust):
        user = reqeust.user
        userprofile = get_object_or_404(UserProfile, user=user)
        
        return Response({f"{user.username} joined in": Channel.objects.filter(participants=userprofile).count()})
    


class ChannelDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ChannelDetailsSerializer
    permission_classes =[permissions.IsAuthenticated]
    queryset = Channel.objects.all()
    lookup_field = 'pk'