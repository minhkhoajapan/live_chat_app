from django.urls import path
from .views import PreloadMessage, CreatChatRoomView, UserInChatRoomValidation, JoinChatRoom, ExitChatRoom, UploadFile, DeleteMessage

urlpatterns = [
    path("load/messages/<str:room_name>/", PreloadMessage.as_view(), name="preload messages"),
    path("create/chatroom/", CreatChatRoomView.as_view(), name="create_chat_room"),
    path("validation/user/chatroom/", UserInChatRoomValidation.as_view(), name="user_in_chat_room"),
    path("join/chatroom/", JoinChatRoom.as_view(), name="join_chat_room"),
    path("exit/chatroom/", ExitChatRoom.as_view(), name='exit_chat_room'),
    path("upload/media/chatroom/", UploadFile.as_view(), name='upload_file_chat_room'),
    path("delete/message/<int:pk>", DeleteMessage.as_view(), name='delete_message'),
]