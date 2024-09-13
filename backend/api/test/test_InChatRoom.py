import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.response import Response
from chat.models import ChatRoom

@pytest.mark.django_db
@pytest.mark.parametrize(
    "usernames, userpasswords, room_name, password",
    [
        (["randomuser1", "randomuser2", "randomuser3"], ["randompass1", "randompass2", "randompass3"], "randomroom", "randomroompass"),
    ],
)
def test_user_in_room_success(usernames, userpasswords, room_name, password):
    create_room_url = reverse('create_chat_room')
    users = [User.objects.create_user(username=username, password=userpassword) for username, userpassword in zip(usernames, userpasswords)]
    room_data = {
        'room_name': room_name, 
        'password': password,
        'usernames': usernames
    }

    #choose the first user to be the room chat creater
    api_client = APIClient()
    refresh_token = RefreshToken.for_user(users[0])
    access_token = str(refresh_token.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    #create room with three users in the room
    api_client.post(create_room_url, data=room_data)

    #make api call to check a user in chat room or not
    check_user_in_room_url = reverse('user_in_chat_room')
    for username in usernames:
        response: Response = api_client.post(check_user_in_room_url, data={'username': username, 'room_name': room_name})
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
@pytest.mark.parametrize(
    "usernames, userpasswords, room_name, password, outside_usernames, outside_user_passwords",
    [
        (["randomuser1", "randomuser2", "randomuser3"], ["randompass1", "randompass2", "randompass3"], "randomroom", "randomroompass", ["randomuser4", "randomuser5"], ["randommpass4", "randompass5"]),
    ],
)
def test_user_in_room_fail(usernames, userpasswords, room_name, password, outside_usernames, outside_user_passwords):
    create_room_url = reverse('create_chat_room')
    users = [User.objects.create_user(username=username, password=userpassword) for username, userpassword in zip(usernames, userpasswords)]
    for username, userpassword in zip(outside_usernames, outside_user_passwords):
        User.objects.create_user(username=username, password=userpassword)

    room_data = {
        'room_name': room_name, 
        'password': password,
        'usernames': usernames
    }

    #choose the first user to be the room chat creater
    api_client = APIClient()
    refresh_token = RefreshToken.for_user(users[0])
    access_token = str(refresh_token.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    #create room with three users in the room
    api_client.post(create_room_url, data=room_data)

    #make api call to check a user in chat room or not
    check_user_in_room_url = reverse('user_in_chat_room')
    for username in outside_usernames:
        response: Response = api_client.post(check_user_in_room_url, data={'username': username, 'room_name': room_name})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
