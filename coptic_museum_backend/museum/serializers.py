from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
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
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'visitor')
        )

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
class LoginUserResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()

# ------------------ Hall ------------------
class HallSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Hall)

    class Meta:
        model = Hall
        fields = ['id', 'number', 'translations']

# ------------------ Artifact ------------------
class ArtifactSerializer(TranslatableModelSerializer):
    hall = HallSerializer(read_only=True)
    hall_id = serializers.PrimaryKeyRelatedField(
        queryset=Hall.objects.all(), source='hall', write_only=True
    )
    translations = TranslatedFieldsField(shared_model=Artifact)

    class Meta:
        model = Artifact
        fields = [
            'id', 'register_number', 'historical_period',
            'province', 'material', 'image', 'created_at',
            'hall', 'hall_id', 'translations'
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
class EventSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Event)

    class Meta:
        model = Event
        fields = ['id', 'translations', 'date', 'location', 'type']

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
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), source='event', write_only=True)
    event_title = serializers.SerializerMethodField()
    event_description = serializers.SerializerMethodField()
    event_date = serializers.DateField(source='event.date', read_only=True)

    def get_event_title(self, obj):
        return obj.event.safe_translation_getter('title', any_language=True)

    def get_event_description(self, obj):
        return obj.event.safe_translation_getter('description', any_language=True)

    class Meta:
        model = Notification
        fields = ['id', 'event_id', 'event_title', 'event_description', 'event_date', 'created_at']

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
class ProgramSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Program)
    artifacts = ArtifactSerializer(many=True, read_only=True)
    artifact_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Artifact.objects.all(), source='artifacts', write_only=True
    )

    class Meta:
        model = Program
        fields = ['id', 'translations', 'artifacts', 'artifact_ids']
