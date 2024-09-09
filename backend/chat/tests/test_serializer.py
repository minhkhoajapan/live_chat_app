import pytest
from django.contrib.auth.models import User
from chat.models import Message
from chat.serializers import MessageSerializer

@pytest.fixture
def test_user() -> User:
    return User.objects.create_user(username="testuser", password="Testpassword123!")

@pytest.fixture
def another_user() -> User:
    return User.objects.create_user(username="anotheruser", password="Testpassword123!")

@pytest.mark.django_db
@pytest.mark.parametrize(
    "message, room_name, sender_name, user_fixture",
    [
        ("Hello", "room1", "testuser", "test_user"),
        ("Hi friend", "room2", "anotheruser", "another_user"),
        ("Hi again", "room3", "testuser", "test_user")
    ],
)
def test_message_deserialization(request, message, room_name, sender_name, user_fixture):
    #Dynamically get the user fixture (test_user or another_user0)
    user: User = request.getfixturevalue(user_fixture)

    data = {
        'message': message,
        'room_name': room_name,
        'sender_name': sender_name
    }

    serializer = MessageSerializer(data=data)
    assert serializer.is_valid()

    #save the deserialized instance
    message_instance = serializer.save()

    assert message_instance.message == message
    assert message_instance.sender == user
    assert message_instance.room_name == room_name

