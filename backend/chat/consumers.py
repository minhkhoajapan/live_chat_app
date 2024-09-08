import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

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
        sender = text_data_jason.get("sender", "Anonymous")

        #Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message, "sender": sender}
        )
 
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))