from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Event, EventBooking
from ..serializers import EventSerializer, BookingSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_event(request):
    user = request.user
    event_id = request.data.get('event')
    
    if EventBooking.objects.filter(user=user, event_id=event_id).exists():
        return Response({'error': 'Already booked this event.'}, status=400)

    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
