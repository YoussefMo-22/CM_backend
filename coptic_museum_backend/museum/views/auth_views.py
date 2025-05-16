from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from ..serializers import UserSerializer

User = get_user_model()

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
        }, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': _('Email and password are required.')}, status=400)

    try:
        user = User.objects.get(email=email)
        if not check_password(password, user.password):
            raise User.DoesNotExist
    except User.DoesNotExist:
        return Response({'error': _('Invalid email or password.')}, status=401)

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
    }, status=200)

class CustomTokenRefreshView(TokenRefreshView):
    pass
