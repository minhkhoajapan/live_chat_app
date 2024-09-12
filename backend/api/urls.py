from django.urls import path
from .views import PreloadMessage

urlpatterns = [
    path("load/messages/<str:room_name>/", PreloadMessage.as_view(), name="preload messages")
]