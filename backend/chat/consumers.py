import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from chat.serializers import MessageSerializer

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        #join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        #Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name) 

    #Receive message from websocket
    async def receive(self, text_data):
        text_data_jason = json.loads(text_data)
        message = text_data_jason["message"]
        sender_name = text_data_jason.get("sender_name", "Anonymous")
        room_name = self.room_name

        self.update_message_db(message=message, sender_name=sender_name, room_name=room_name)

        #Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message, "sender_name": sender_name, "room_name": room_name}
        )
 
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender_name"]
        room_name = event["room_name"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender_name": sender, "room_name": room_name}))
    
    def update_message_db(self, message, sender_name, room_name):
        message_serializer = MessageSerializer(data= {
            "message": message,
            "sender_name": sender_name,
            "room_name": room_name
        })

        if message_serializer.is_valid():
            message_serializer.save()