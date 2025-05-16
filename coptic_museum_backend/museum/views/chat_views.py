from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import ChatLog
from ..serializers import ChatLogSerializer
import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rasa_chat(request):
    message = request.data.get("message")
    # Simulated Rasa response
    bot_response = "This is a placeholder Rasa response to: " + message

    ChatLog.objects.create(user=request.user, message=message, response=bot_response)

    return Response({"response": bot_response})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_logs(request):
    logs = ChatLog.objects.filter(user=request.user)
    serializer = ChatLogSerializer(logs, many=True)
    return Response(serializer.data)
