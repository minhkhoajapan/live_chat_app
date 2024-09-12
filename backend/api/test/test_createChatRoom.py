import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

@pytest.fixture
def authorized_client() -> APIClient:

    api_client = APIClient()
    user = User.objects.create_user(username='randomuser', password='randomuser')

    #Manually generate refresh and access_token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client

@pytest.mark.django_db
@pytest.mark.parametrize(
    "room_name, password",
    [
        ("topscret", "gaypassword123"),
        ("agents of shields", "marvel123!"),
        ("the_Illuminati", "ruletheworl2435")
    ],
)
def test_create_chat_room_success(authorized_client,room_name, password):
    url = reverse('create_chat_room')
    data = {
        'room_name': room_name,
        'password': password
    }
    response: Response = authorized_client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
