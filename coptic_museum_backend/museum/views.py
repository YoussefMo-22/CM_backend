# # from rest_framework.response import Response
# # from rest_framework.decorators import api_view
# # from .models import Artifact
# # from .serializers import ArtifactSerializer
# # from .models import ChatLog
# # from django.contrib.auth import get_user_model
# # from django.contrib.auth.hashers import check_password
# # from rest_framework.decorators import api_view
# # from rest_framework.response import Response
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from django.contrib.auth.models import User
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from .serializers import UserSerializer

# # from django.utils import translation
# # from django.utils.translation import gettext as _
# # from django_ratelimit.decorators import ratelimit
# # from rest_framework.decorators import api_view, permission_classes
# # from rest_framework.permissions import IsAuthenticated
# # from rest_framework.response import Response
# # import requests

# # @api_view(['POST'])
# # def register_user(request):
# #     serializer = UserSerializer(data=request.data)
# #     if serializer.is_valid():
# #         user = serializer.save()
# #         refresh = RefreshToken.for_user(user)
# #         return Response({
# #             'refresh': str(refresh),
# #             'access': str(refresh.access_token),
# #             'user': serializer.data
# #         })
# #     return Response(serializer.errors, status=400)


# # from django.contrib.auth import authenticate


# # from django.contrib.auth import get_user_model
# # from django.contrib.auth.hashers import check_password
# # from rest_framework.decorators import api_view, permission_classes, authentication_classes
# # from rest_framework.permissions import AllowAny
# # from rest_framework.authentication import BasicAuthentication
# # from rest_framework.response import Response
# # from rest_framework import status
# # from rest_framework_simplejwt.tokens import RefreshToken

# # User = get_user_model()

# # @api_view(['POST'])
# # @permission_classes([AllowAny])  # Anyone can access this endpoint
# # @authentication_classes([])      # No token required to access
# # def login_user(request):
# #     email = request.data.get('email')
# #     password = request.data.get('password')

# #     # Input validation
# #     if not email or not password:
# #         return Response(
# #             {'error': 'Email and password are required.'},
# #             status=status.HTTP_400_BAD_REQUEST
# #         )

# #     try:
# #         user = User.objects.get(email=email)
# #     except User.DoesNotExist:
# #         return Response(
# #             {'error': 'Invalid email or password.'},
# #             status=status.HTTP_401_UNAUTHORIZED
# #         )

# #     if not check_password(password, user.password):
# #         return Response(
# #             {'error': 'Invalid email or password.'},
# #             status=status.HTTP_401_UNAUTHORIZED
# #         )

# #     # Optional: check if user is active
# #     if not user.is_active:
# #         return Response(
# #             {'error': 'User account is disabled.'},
# #             status=status.HTTP_403_FORBIDDEN
# #         )

# #     # Generate JWT tokens
# #     refresh = RefreshToken.for_user(user)

# #     return Response({
# #         'message': 'Login successful',
# #         'access': str(refresh.access_token),
# #         'refresh': str(refresh),
# #         'user': {
# #             'id': user.id,
# #             'email': user.email,
# #             'username': user.username,
# #         }
# #     }, status=status.HTTP_200_OK)




# # from rest_framework_simplejwt.views import TokenRefreshView

# # class CustomTokenRefreshView(TokenRefreshView):
# #     pass


# # @api_view(['GET'])
# # def get_artifacts(request):
# #     artifacts = Artifact.objects.all()
# #     serializer = ArtifactSerializer(artifacts, many=True)
# #     return Response(serializer.data)

# # @api_view(['GET', 'POST'])
# # def artifacts_list_create(request):
# #     if request.method == 'GET':
# #         artifacts = Artifact.objects.all()
# #         serializer = ArtifactSerializer(artifacts, many=True)
# #         return Response(serializer.data)

# #     elif request.method == 'POST':
# #         serializer = ArtifactSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=201)
# #         return Response(serializer.errors, status=400)

# # @api_view(['GET', 'PUT', 'DELETE'])
# # def artifact_detail(request, pk):
# #     try:
# #         artifact = Artifact.objects.get(pk=pk)
# #     except Artifact.DoesNotExist:
# #         return Response({'error': 'Artifact not found'}, status=404)

# #     if request.method == 'GET':
# #         serializer = ArtifactSerializer(artifact)
# #         return Response(serializer.data)

# #     elif request.method == 'PUT':
# #         serializer = ArtifactSerializer(artifact, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=400)

# #     elif request.method == 'DELETE':
# #         artifact.delete()
# #         return Response({'message': 'Artifact deleted'}, status=204)


# # from .models import Event
# # from .serializers import EventSerializer

# # @api_view(['GET'])
# # def get_events(request):
# #     events = Event.objects.all()
# #     serializer = EventSerializer(events, many=True)
# #     return Response(serializer.data)


# # import requests
# # from rest_framework.response import Response
# # from rest_framework.decorators import api_view

# # from rest_framework.decorators import api_view, permission_classes
# # from rest_framework.permissions import IsAuthenticated
# # from rest_framework.response import Response
# # from .models import ChatLog
# # import requests


# # from drf_yasg.utils import swagger_auto_schema
# # from drf_yasg import openapi

# # @swagger_auto_schema(
# #     method='post',
# #     request_body=openapi.Schema(
# #         type=openapi.TYPE_OBJECT,
# #         required=['message'],
# #         properties={
# #             'message': openapi.Schema(type=openapi.TYPE_STRING)
# #         }
# #     ),
# #     responses={200: 'Chatbot response'}
# # )



# # @ratelimit(key='user', rate='5/m', block=True)  # 5 requests per minute per user
# # @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# # def rasa_chat(request):
# #     user = request.user
# #     user_id = str(user.id)
# #     username = user.username
# #     user_message = request.data.get("message")
    
# #     # Set language from header, default to 'en'
# #     lang = request.headers.get("Accept-Language", "en")
# #     translation.activate(lang)

# #     if not user_message:
# #         return Response({"error": _("Message is required.")}, status=400)

# #     rasa_url = "http://127.0.0.1:5005/webhooks/rest/webhook"

# #     try:
# #         response = requests.post(rasa_url, json={"sender": user_id, "message": user_message})
        
# #         if response.status_code == 200:
# #             bot_response = response.json()
# #             messages = [msg.get('text') for msg in bot_response if 'text' in msg]
# #             return Response({
# #                 "status": _("success"),
# #                 "user_id": user_id,
# #                 "username": username,
# #                 "messages": messages or [_("No response from bot.")]
# #             })
# #         else:
# #             return Response({"error": _("Rasa server error.")}, status=500)
# #     except requests.exceptions.RequestException as e:
# #         return Response({"error": _("Could not connect to chatbot.") + f" {str(e)}"}, status=500)





# # import tensorflow as tf
# # import numpy as np
# # import cv2
# # from django.http import JsonResponse
# # from django.views.decorators.csrf import csrf_exempt

# # # Load pre-trained AI model
# # # model = tf.keras.models.load_model("artifact_model.h5")  # Adjust your model path   ابقى شيلها بعدين

# # @csrf_exempt
# # def identify_artifact(request):
# #     if request.method == 'POST' and request.FILES.get('image'):
# #         image = request.FILES['image']

# #         # Convert image to format compatible with model
# #         image_data = np.asarray(bytearray(image.read()), dtype=np.uint8)
# #         image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
# #         image = cv2.resize(image, (224, 224)) / 255.0  # Resize and normalize
# #         image = np.expand_dims(image, axis=0)

# #         # Predict artifact
# #         predictions = model.predict(image)
# #         artifact_name = np.argmax(predictions)  # Convert model output to artifact name

# #         return JsonResponse({"artifact_name": artifact_name})

# #     return JsonResponse({"error": "Invalid request"}, status=400)


# # @api_view(['POST'])
# # def upload_artifact_image(request):
# #     if request.method == 'POST':
# #         serializer = ArtifactSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Standard Library
# import numpy as np
# import cv2
# import requests

# # Django
# from django.http import JsonResponse
# from django.utils import translation
# from django.utils.translation import gettext as _
# from django.views.decorators.csrf import csrf_exempt

# # Django REST Framework
# from rest_framework import status
# from rest_framework.decorators import (
#     api_view, permission_classes, authentication_classes
# )
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.authentication import BasicAuthentication
# from rest_framework.response import Response

# # JWT Auth
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.views import TokenRefreshView

# # Ratelimit
# from django_ratelimit.decorators import ratelimit

# # Swagger
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

# # Local Imports
# from .models import Artifact, ChatLog, Event
# from .serializers import ArtifactSerializer, UserSerializer, EventSerializer
# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import check_password

# # AI model (uncomment when ready)
# # model = tf.keras.models.load_model("artifact_model.h5")

# User = get_user_model()


# # ─────────────────────────────────────────────────────────────────────────────
# # AUTH VIEWS
# # ─────────────────────────────────────────────────────────────────────────────

# @api_view(['POST'])
# @permission_classes([AllowAny])
# @authentication_classes([])
# def register_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'user': serializer.data
#         }, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# @authentication_classes([])
# def login_user(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     if not email or not password:
#         return Response({'error': _('Email and password are required.')},
#                         status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.get(email=email)
#         if not check_password(password, user.password):
#             raise User.DoesNotExist
#     except User.DoesNotExist:
#         return Response({'error': _('Invalid email or password.')},
#                         status=status.HTTP_401_UNAUTHORIZED)

#     if not user.is_active:
#         return Response({'error': _('User account is disabled.')},
#                         status=status.HTTP_403_FORBIDDEN)

#     refresh = RefreshToken.for_user(user)
#     return Response({
#         'message': _('Login successful'),
#         'access': str(refresh.access_token),
#         'refresh': str(refresh),
#         'user': {
#             'id': user.id,
#             'email': user.email,
#             'username': user.username,
#         }
#     }, status=status.HTTP_200_OK)


# class CustomTokenRefreshView(TokenRefreshView):
#     pass


# # ─────────────────────────────────────────────────────────────────────────────
# # ARTIFACT VIEWS
# # ─────────────────────────────────────────────────────────────────────────────

# @api_view(['GET', 'POST'])
# def artifacts_list_create(request):
#     if request.method == 'GET':
#         artifacts = Artifact.objects.all()
#         serializer = ArtifactSerializer(artifacts, many=True)
#         return Response(serializer.data)

#     serializer = ArtifactSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def artifact_detail(request, pk):
#     try:
#         artifact = Artifact.objects.get(pk=pk)
#     except Artifact.DoesNotExist:
#         return Response({'error': _('Artifact not found')}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = ArtifactSerializer(artifact)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = ArtifactSerializer(artifact, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         artifact.delete()
#         return Response({'message': _('Artifact deleted')}, status=status.HTTP_204_NO_CONTENT)


# @api_view(['POST'])
# def upload_artifact_image(request):
#     serializer = ArtifactSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# def identify_artifact(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image_file = request.FILES['image']
#         image_data = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
#         image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
#         image = cv2.resize(image, (224, 224)) / 255.0
#         image = np.expand_dims(image, axis=0)

#         # predictions = model.predict(image)
#         # artifact_name = np.argmax(predictions)

#         artifact_name = "DummyArtifact"  # Replace when model is loaded
#         return JsonResponse({"artifact_name": artifact_name})

#     return JsonResponse({"error": _("Invalid request")}, status=400)


# # ─────────────────────────────────────────────────────────────────────────────
# # EVENT VIEWS
# # ─────────────────────────────────────────────────────────────────────────────

# @api_view(['GET'])
# def get_events(request):
#     events = Event.objects.all()
#     serializer = EventSerializer(events, many=True)
#     return Response(serializer.data)


# # ─────────────────────────────────────────────────────────────────────────────
# # CHATBOT (RASA) VIEWS
# # ─────────────────────────────────────────────────────────────────────────────

# @swagger_auto_schema(
#     method='post',
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         required=['message'],
#         properties={
#             'message': openapi.Schema(type=openapi.TYPE_STRING)
#         }
#     ),
#     responses={200: 'Chatbot response'}
# )
# @ratelimit(key='user', rate='5/m', block=True)
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def rasa_chat(request):
#     user = request.user
#     user_id = str(user.id)
#     user_message = request.data.get("message")

#     lang = request.headers.get("Accept-Language", "en")
#     translation.activate(lang)

#     if not user_message:
#         return Response({"error": _("Message is required.")}, status=status.HTTP_400_BAD_REQUEST)

#     rasa_url = "http://127.0.0.1:5005/webhooks/rest/webhook"

#     try:
#         rasa_response = requests.post(rasa_url, json={"sender": user_id, "message": user_message})
#         if rasa_response.status_code == 200:
#             bot_data = rasa_response.json()
#             messages = [msg.get('text') for msg in bot_data if 'text' in msg]
#             return Response({
#                 "status": _("success"),
#                 "user_id": user_id,
#                 "username": user.username,
#                 "messages": messages or [_("No response from bot.")]
#             })
#         return Response({"error": _("Rasa server error.")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     except requests.exceptions.RequestException as e:
#         return Response({"error": _("Could not connect to chatbot.") + f" {str(e)}"},
#                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Artifact, Event, Program, Artifact3DModel, Notification, InteractiveMap
from .serializers import (
    ArtifactSerializer, EventSerializer, ProgramSerializer,
    Artifact3DModelSerializer, NotificationSerializer, InteractiveMapSerializer
)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff


class ArtifactViewSet(viewsets.ModelViewSet):
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['get'], url_path='hall/(?P<hall_name>[^/.]+)')
    def get_by_hall(self, request, hall_name=None):
        artifacts = self.queryset.filter(hall__iexact=hall_name)
        serializer = self.get_serializer(artifacts, many=True)
        return Response({"success": True, "data": serializer.data})


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        event = serializer.save()
        Notification.objects.create(title="New Event Added", message=event.title)


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAdminOrReadOnly]


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


import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .utils.auth import require_token

@require_token
@csrf_exempt
def ask_chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question")
            artifact_name = data.get("artifact")  # Optional
            image_url = data.get("image_url")     # Optional in case of image upload

            if not question:
                return JsonResponse({"error": "Question is required"}, status=400)

            # Build payload
            payload = {
                "query": question
            }

            if artifact_name:
                payload["artifact"] = artifact_name
            if image_url:
                payload["image_url"] = image_url

            # Send to FastAPI
            response = requests.post("http://localhost:8001/ask", json=payload)
            response.raise_for_status()

            return JsonResponse(response.json())

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except requests.RequestException as e:
            return JsonResponse({"error": "Failed to contact chatbot API", "details": str(e)}, status=500)

    return JsonResponse({"error": "POST request required"}, status=405)




import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.auth import require_token

@require_token
@csrf_exempt  # if you test with Postman or frontend separately, remove if you handle CSRF in frontend
def identify_artifact(request):
    if request.method == "POST" and request.FILES.get('image'):
        image_file = request.FILES['image']

        # Prepare files dict for requests
        files = {'file': (image_file.name, image_file.read(), image_file.content_type)}

        # Call FastAPI chatbot endpoint
        try:
            response = requests.post('http://localhost:8001/identify-artifact', files=files)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            return JsonResponse({"error": "Failed to connect to chatbot API", "details": str(e)}, status=500)

        return JsonResponse(data)
    return JsonResponse({"error": "POST request with image file required"}, status=400)
