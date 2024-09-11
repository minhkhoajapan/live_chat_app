from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from chat.models import Message
from chat.serializers import MessageSerializer

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