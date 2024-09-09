from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only = True)
    sender_name = serializers.CharField(write_only = True)

    class Meta:
        model = Message
        fields = ['message', 'sender', 'sender_name' 'room_name', 'timestamp']
    
    def create(self, validated_data):
        sender_name = validated_data.pop('sender_name')
        try:
            sender = User.objects.get(username=sender_name)
        except User.DoesNotExist:
            raise serializers.ValidationError({'sender_name: User with this username does not exist'})

        validated_data['sender'] = sender
        return super.create(validated_data)

