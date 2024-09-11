from django.urls import path
from .views import PreloadMessage

urlpatterns = [
    path("<str:room_name>/", PreloadMessage.as_view(), name="preload messages")
]