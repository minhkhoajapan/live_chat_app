import pytest
from django.contrib.auth.models import User
from ..models import Message
from ..serializers import MessageSerializer
from datetime import datetime

@pytest.fixture
def test_user() -> User:
    return User.objects.create_user(username="testuser", password="Testpassword123!")

@pytest.fixture
def another_user() -> User:
    return User.objects.create_user(username="anotheruser", password="Testpassword123!")

@pytest.mark.parametrize(
    "message, room_name, user_fixture",
    [
        ("Hello", "room1", "test_user"),
        ("Hi friend, room2, another_user"),
        ("Hi again", "room3", "test_user")
    ],
)
def test_message_deserialization(request, message, room_name, user_fixture):
    #Dynamically get the user fixture (test_user or another_user0)
    user: User = request.getfixturevalue(user_fixture)

    data = {
        'message': message,
        'room_name': room_name,
        'sender': user.username
    }
