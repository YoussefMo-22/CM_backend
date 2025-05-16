from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import InteractiveMap
from ..serializers import InteractiveMapSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_map_data(request):
    map_data = InteractiveMap.objects.all()
    serializer = InteractiveMapSerializer(map_data, many=True)
    return Response(serializer.data)
