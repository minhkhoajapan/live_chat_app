from django.urls import path
from .views import PreloadMessage, CreatChatRoomView, UserInChatRoomValidation, JoinChatRoom

urlpatterns = [
    path("load/messages/<str:room_name>/", PreloadMessage.as_view(), name="preload messages"),
    path("create/chatroom/", CreatChatRoomView.as_view(), name="create_chat_room"),
    path("validation/user/chatroom/", UserInChatRoomValidation.as_view(), name="user_in_chat_room"),
    path("join/chatroom/", JoinChatRoom.as_view(), name="join_chat_room"),
]