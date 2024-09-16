from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from chat.models import ChatRoom
import pytest

@pytest.fixture
def user1() -> User:
    user = User.objects.create_user(username="user1", password="password1")
    return user

@pytest.fixture
def api_client_user1(user1) -> APIClient:
    api_client = APIClient()
    refresh = RefreshToken.for_user(user1)
    access_token = str(refresh.access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client

@pytest.fixture
def my_chat_room(api_client_user1) -> ChatRoom:
    create_room_url = reverse('create_chat_room')
    data = {
        'room_name': 'my_chat_room',
        'password': 'myroompassword',
        'usernames': ['user1'],
    }
    api_client_user1.post(create_room_url, data=data)
    chat_room = ChatRoom.objects.get(room_name='my_chat_room')
    return chat_room

@pytest.mark.django_db
@pytest.mark.parametrize(
    'usernames, passwords',
    [
        (['user2', 'user3', 'user4'], ['password2', 'password3', 'password4']),
    ],
)
def test_exit_chat_room_success(usernames, passwords, my_chat_room):
    users = [User.objects.create_user(username=username, password=password) for username, password in zip(usernames, passwords)]
    join_chat_room_url = reverse("join_chat_room")

    for user in users:
        api_client = APIClient()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        res: Response = api_client.post(join_chat_room_url, data={
            'username': user.username,
            'room_name': 'my_chat_room',
            'password': 'myroompassword',
        })
        assert res.status_code == status.HTTP_200_OK
        assert my_chat_room.authenticated_member.filter(id=user.id).exists() == True

    exit_chat_room_url = reverse("exit_chat_room")
    for user in users:
        api_client = APIClient()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        res: Response = api_client.post(exit_chat_room_url, data={
            'username': user.username,
            'room_name': 'my_chat_room',
        })
        assert res.status_code == status.HTTP_200_OK
        assert my_chat_room.authenticated_member.filter(id=user.id).exists() == False