from rest_framework import serializers
from .models import Message, ChatRoom
from django.contrib.auth.models import User
from typing import List

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'message', 'sender', 'sender_username', 'room_name', 'timestamp', 'file']
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

class ChatRoomSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    usernames = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = ChatRoom
        fields = ['room_name', 'password', 'usernames']
    
    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        authenticated_member_usernames: List = validated_data.pop('usernames', [])
        chat_room = ChatRoom(**validated_data)
        chat_room.set_password(raw_password)
        chat_room.save()

        authenticated_members = [User.objects.get(username=member_username) for member_username in authenticated_member_usernames]
        chat_room.authenticated_member.set(authenticated_members)

        return chat_room