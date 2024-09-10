from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(write_only=True)

    class Meta:
        model = Message
        fields = ['message', 'sender', 'sender_username', 'room_name', 'timestamp']
        extra_kwargs = {
            'sender': {'read_only': True}
        }
    
    def create(self, validated_data):
        sender_username = validated_data.pop('sender_username')
        try:
            sender = User.objects.get(username=sender_username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'sender_username: User with this username does not exist'})

        validated_data['sender'] = sender
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        sender = instance.sender

        representation['sender'] = {
            'username': sender.username,
        }

        return representation
