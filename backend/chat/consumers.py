import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from chat.serializers import MessageSerializer
from channels.db import database_sync_to_async

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
        print(text_data_jason)
        message = text_data_jason["message"]
        sender_username = text_data_jason.get("sender_username", "Anonymous")
        room_name = self.room_name
        
        message_serializer = await self.update_message_db(message, sender_username, room_name)
        data = message_serializer.data

        #Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "data": data}
        )
 
    async def chat_message(self, event):
        data = event["data"]
        # Send message to WebSocket 
        await self.send(text_data=json.dumps({**data}))
    
    async def update_message_db(self, message, sender_username, room_name) -> MessageSerializer:
        message_serializer = await database_sync_to_async(self._update_message_db_helper)(message, sender_username, room_name)
        return message_serializer

    def _update_message_db_helper(self, message, sender_username, room_name) -> MessageSerializer:
        message_serializer = MessageSerializer(data= {
            "message": message,
            "sender_username": sender_username,
            "room_name": room_name
        })

        if message_serializer.is_valid():
            message_serializer.save()
        else:
            raise ValueError("Invalid data for message serializer")
        
        return message_serializer
    