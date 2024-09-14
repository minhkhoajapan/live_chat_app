from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer
from chat.models import Message, ChatRoom
from chat.serializers import MessageSerializer, ChatRoomSerializer
from django.db import IntegrityError

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

#class view to return messages that was stored in database (for each room_name)
class PreloadMessage(APIView):
    def get(self, request, room_name):
        messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class CreatChatRoomView(APIView):
    def post(self, request):
        serializer = ChatRoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInChatRoomValidation(APIView):
    def post(self, request):
        username = request.data['username']
        room_name = request.data['room_name']
        
        try:
            user: User = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "This user does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            chat_room: ChatRoom = ChatRoom.objects.get(room_name=room_name)
        except ChatRoom.DoesNotExist:
            return Response({"detail": "This chat room does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        if chat_room.authenticated_member.filter(id=user.id).exists():
            return Response({"detail": "This user is in the chat room."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "This user is not in the chat room."}, status=status.HTTP_401_UNAUTHORIZED)

class JoinChatRoom(APIView):
    def post(self, request):
        username = request.data['username']
        room_name = request.data['room_name']
        password = request.data['password']

        try:
            user: User = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "This user does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            chat_room: ChatRoom = ChatRoom.objects.get(room_name=room_name)
        except ChatRoom.DoesNotExist:
            return Response({"detail": "This chat room does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        if chat_room.verify_password(password):
            chat_room.authenticated_member.add(user)
            return Response({"detail": "Chat room authentication succeed."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Chat room authentication failed."}, status=status.HTTP_401_UNAUTHORIZED)