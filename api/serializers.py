from editor.models import Channel, UserProfile
from rest_framework import generics
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'profile_picture']

class ChannelSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    
    created_by = UserProfileSerializer(read_only=True)

    class Meta:
        model = Channel
        fields = ['id', 'name', 'channel_picture', 'programing_language',
                  'created_by', 'participants', 'created_at', 'updated_at']

    def get_participants(self, obj):
        # Limit to first 5 participants
        participants = obj.participants.all()[:5]
        
        return UserProfileSerializer(participants, many=True).data

class JoinChannelSerializer(serializers.ModelSerializer):
    channel_id = serializers.CharField(write_only=True)
    class Meta:
        model = Channel
        fields = ['id', 'channel_id']
        

from editor.models import CodeFile
class CodeFileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = CodeFile
        fields = '__all__'

class ChannelDetailsSerializer(serializers.ModelSerializer):
    channel_details = serializers.SerializerMethodField(read_only=True)
    channels_files = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Channel
        fields = [
            'channel_details',
            'channels_files'
        ]
        
    def get_channel_details(self, obj):
        
        return ChannelSerializer(obj).data
    
    def get_channels_files(self, obj):
        codefiles = CodeFile.objects.filter(channel=obj)
        if not codefiles:
            return {"detail":"No files found in this channel"}
        return CodeFileSerializer(codefiles, many=True).data