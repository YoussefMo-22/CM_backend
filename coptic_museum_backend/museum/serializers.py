from rest_framework import serializers
from .models import (
    User, Artifact, Artifact3DModel, Event, EventBooking,
    ChatLog, Notification, InteractiveMap, Program, Hall
)

# ------------------ User ------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'visitor')
        )
        return user

# ------------------ Hall ------------------
class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ['id', 'number', 'name']

# ------------------ Artifact ------------------
class ArtifactSerializer(serializers.ModelSerializer):
    hall = HallSerializer(read_only=True)
    hall_id = serializers.PrimaryKeyRelatedField(
        queryset=Hall.objects.all(), source='hall', write_only=True
    )

    class Meta:
        model = Artifact
        fields = [
            'id', 'register_number', 'name', 'description', 'historical_period',
            'province', 'material', 'image', 'hall', 'hall_id', 'created_at'
        ]

# ------------------ Artifact 3D Model ------------------
class Artifact3DModelSerializer(serializers.ModelSerializer):
    artifact = ArtifactSerializer(read_only=True)
    artifact_id = serializers.PrimaryKeyRelatedField(
        queryset=Artifact.objects.all(), source='artifact', write_only=True
    )

    class Meta:
        model = Artifact3DModel
        fields = ['id', 'artifact', 'artifact_id', 'model_file', 'description']

# ------------------ Event ------------------
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'type']

# ------------------ Event Booking ------------------
class EventBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), source='event', write_only=True
    )

    class Meta:
        model = EventBooking
        fields = ['id', 'user', 'user_id', 'event', 'event_id']

# ------------------ Notification ------------------
class NotificationSerializer(serializers.ModelSerializer):
    # Directly include related event fields in the notification response
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), source='event', write_only=True)
    event_name = serializers.CharField(source='event.title', read_only=True)
    event_description = serializers.CharField(source='event.description', read_only=True)
    event_date = serializers.DateField(source='event.date', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'event_id', 'event_name', 'event_description', 'event_date', 'created_at']

# ------------------ Chat Log ------------------
class ChatLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = ChatLog
        fields = ['id', 'user', 'user_id', 'user_message', 'bot_response', 'timestamp']

# ------------------ Interactive Map ------------------
class InteractiveMapSerializer(serializers.ModelSerializer):
    hall = HallSerializer(read_only=True)
    hall_id = serializers.PrimaryKeyRelatedField(
        queryset=Hall.objects.all(), source='hall', write_only=True
    )

    class Meta:
        model = InteractiveMap
        fields = ['id', 'hall', 'hall_id', 'x_coordinate', 'y_coordinate']

# ------------------ Program ------------------
class ProgramSerializer(serializers.ModelSerializer):
    artifacts = ArtifactSerializer(many=True, read_only=True)
    artifact_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Artifact.objects.all(), source='artifacts', write_only=True
    )

    class Meta:
        model = Program
        fields = ['id', 'title', 'description', 'artifacts', 'artifact_ids']
