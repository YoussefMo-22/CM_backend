# Django REST Framework
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import (
    api_view, permission_classes, authentication_classes, action
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response

# JWT Auth
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

# Ratelimit
from django_ratelimit.decorators import ratelimit

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Django utils
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext as _

# External API
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Parler
from parler.utils.context import switch_language

# Local Imports
from .models import (
    Artifact, ChatLog, Event, Program, Artifact3DModel,
    Notification, InteractiveMap, Hall
)
from .serializers import (
    ArtifactSerializer, UserSerializer, EventSerializer,
    ProgramSerializer, Artifact3DModelSerializer,
    NotificationSerializer, InteractiveMapSerializer, HallSerializer,
    RegisterSerializer, LoginSerializer, LoginUserResponseSerializer
)
from .utils.auth import require_token

User = get_user_model()


# ─────────────────────────────────────────────────────────────────────────────
# AUTH VIEWS
# ─────────────────────────────────────────────────────────────────────────────

@swagger_auto_schema(method='post', request_body=RegisterSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=LoginSerializer, responses={200: LoginUserResponseSerializer})
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': _('Email and password are required.')},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        if not check_password(password, user.password):
            raise User.DoesNotExist
    except User.DoesNotExist:
        return Response({'error': _('Invalid email or password.')},
                        status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({'error': _('User account is disabled.')},
                        status=status.HTTP_403_FORBIDDEN)

    refresh = RefreshToken.for_user(user)
    return Response({
        'message': _('Login successful'),
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
        }
    }, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    pass


# ─────────────────────────────────────────────────────────────────────────────
# PERMISSIONS
# ─────────────────────────────────────────────────────────────────────────────

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff


# ─────────────────────────────────────────────────────────────────────────────
# VIEWSETS
# ─────────────────────────────────────────────────────────────────────────────

class ArtifactViewSet(viewsets.ModelViewSet):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        lang = self.request.LANGUAGE_CODE
        return self.queryset.active_translations(lang)

    @action(detail=False, methods=['get'], url_path='hall/(?P<hall_name>[^/.]+)')
    def get_by_hall(self, request, hall_name=None):
        language = request.GET.get('lang') or request.LANGUAGE_CODE
        with switch_language(Hall, language):
            artifacts = self.queryset.filter(
                hall__translations__language_code=language,
                hall__translations__name__iexact=hall_name
            )
            serializer = self.get_serializer(artifacts, many=True)
            return Response({"success": True, "data": serializer.data})


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        lang = self.request.LANGUAGE_CODE
        return self.queryset.active_translations(lang)

    def perform_create(self, serializer):
        event = serializer.save()
        Notification.objects.create(title="New Event Added", message=event.title)


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        lang = self.request.LANGUAGE_CODE
        return self.queryset.active_translations(lang)


class ThreeDModelViewSet(viewsets.ModelViewSet):
    queryset = Artifact3DModel.objects.all()
    serializer_class = Artifact3DModelSerializer
    permission_classes = [IsAdminOrReadOnly]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrReadOnly]


class MapDataViewSet(viewsets.ModelViewSet):
    queryset = InteractiveMap.objects.all()
    serializer_class = InteractiveMapSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        lang = self.request.LANGUAGE_CODE
        return self.queryset.active_translations(lang)


class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        lang = self.request.LANGUAGE_CODE
        return self.queryset.active_translations(lang)


# ─────────────────────────────────────────────────────────────────────────────
# CHATBOT INTEGRATION
# ─────────────────────────────────────────────────────────────────────────────

@require_token
@csrf_exempt
def ask_chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question")
            artifact_name = data.get("artifact")
            image_url = data.get("image_url")

            if not question:
                return JsonResponse({"error": "Question is required"}, status=400)

            payload = {"query": question}
            if artifact_name:
                payload["artifact"] = artifact_name
            if image_url:
                payload["image_url"] = image_url

            response = requests.post("http://localhost:8001/ask", json=payload)
            response.raise_for_status()

            return JsonResponse(response.json())

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except requests.RequestException as e:
            return JsonResponse({"error": "Failed to contact chatbot API", "details": str(e)}, status=500)

    return JsonResponse({"error": "POST request required"}, status=405)


@require_token
@csrf_exempt
def identify_artifact(request):
    if request.method == "POST" and request.FILES.get('image'):
        image_file = request.FILES['image']
        files = {'file': (image_file.name, image_file.read(), image_file.content_type)}

        try:
            response = requests.post('http://localhost:8001/identify-artifact', files=files)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            return JsonResponse({"error": "Failed to connect to chatbot API", "details": str(e)}, status=500)

        return JsonResponse(data)
    return JsonResponse({"error": "POST request with image file required"}, status=400)
