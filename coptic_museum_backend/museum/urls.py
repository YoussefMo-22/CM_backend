# from django.urls import path # type: ignore
# from .views import get_artifacts, get_events, artifacts_list_create, artifact_detail
from .views import register_user, login_user, CustomTokenRefreshView
# from .views import rasa_chat
# from .views import upload_artifact_image
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Coptic Museum API",
#         default_version='v1',
#         description="Chatbot + Auth API",
#         contact=openapi.Contact(email="your@email.com"),
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
# )

# urlpatterns = [
#     path('artifacts/', get_artifacts, name="get_artifacts"),
#     path('events/', get_events, name="get_events"),
#     path('auth/register/', register_user, name="register"),
#     path('auth/login/', login_user, name="login"),
#     path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh"),
#     path('chat/', rasa_chat, name="rasa_chat"),
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     path('api/artifacts/upload/', upload_artifact_image, name='upload_artifact_image')
# ]

# urlpatterns += [
#     path('artifacts/', artifacts_list_create, name="artifacts_list_create"),
#     path('artifacts/<int:pk>/', artifact_detail, name="artifact_detail"),
# ]

# from .views import identify_artifact

# urlpatterns += [
#     path('identify_artifact/', identify_artifact, name="identify_artifact"),
# ]

# Enhanced Django views and urls.py to support full Coptic Museum functionalities
# including interactive map, 3D models, programs, chat logs, notifications, event bookings

from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# # Import views
# from .views.auth_views import register_user, login_user, CustomTokenRefreshView
# from .views.artifact_views import artifacts_list_create, artifact_detail, upload_artifact_image, identify_artifact, get_3d_models
# from .views.event_views import get_events, book_event
# from .views.chat_views import rasa_chat, get_chat_logs
# from .views.notification_views import get_notifications
# from .views.map_views import get_map_data
# from .views.program_views import get_programs


# # Swagger config
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Coptic Museum API",
#         default_version="v1",
#         description="Coptic Museum API - Artifacts, Events, Users, Interactive Map, and Chatbot",
#         contact=openapi.Contact(email="your@email.com"),
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
# )

# urlpatterns = [
    # Auth
    # path('auth/register/', register_user, name="register"),
    # path('auth/login/', login_user, name="login"),
    # path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh"),

#     # Artifacts
#     path('artifacts/', artifacts_list_create, name="artifacts_list_create"),
#     path('artifacts/<int:pk>/', artifact_detail, name="artifact_detail"),
#     path('artifacts/upload/', upload_artifact_image, name='upload_artifact_image'),

#     # AI Image Identifier
#     path('identify_artifact/', identify_artifact, name="identify_artifact"),

#     # Events & Workshops
#     path('events/', get_events, name="get_events"),
#     path('events/book/', book_event, name="book_event"),

#     # Chatbot
#     path('chat/', rasa_chat, name="rasa_chat"),

#     # Chat Logs
#     path('chat/logs/', get_chat_logs, name="get_chat_logs"),

#     # Notifications
#     path('notifications/', get_notifications, name="get_notifications"),

#     # Interactive Map
#     path('map/', get_map_data, name="interactive_map"),

#     # 3D Models
#     path('artifacts/3d/', get_3d_models, name="get_3d_models"),

#     # Suggested Tours (Programs)
#     path('programs/', get_programs, name="get_programs"),
#     # path('programs/<int:pk>/', get_program_detail, name="get_program_detail"),

#     # API Docs
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]

from rest_framework.routers import DefaultRouter
from .views import (
    ArtifactViewSet, EventViewSet, ProgramViewSet,
    ThreeDModelViewSet, NotificationViewSet, MapDataViewSet
)
from .views import identify_artifact
from .views import ask_chatbot

router = DefaultRouter()
router.register('artifacts', ArtifactViewSet, basename='artifact')
router.register('events', EventViewSet, basename='event')
router.register('programs', ProgramViewSet, basename='program')
router.register('3d-models', ThreeDModelViewSet, basename='3dmodel')
router.register('notifications', NotificationViewSet, basename='notification')
router.register('map-data', MapDataViewSet, basename='mapdata')

urlpatterns = router.urls

urlpatterns += [
    # Auth
    path('auth/register/', register_user, name="register"),
    path('auth/login/', login_user, name="login"),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh"),
    path('identify-artifact/', identify_artifact, name='identify_artifact'),
    path('ask-chatbot/', ask_chatbot, name='ask_chatbot'),
]