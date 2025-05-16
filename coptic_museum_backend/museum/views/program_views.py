from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Program
from ..serializers import ProgramSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_programs(request):
    programs = Program.objects.all()
    serializer = ProgramSerializer(programs, many=True)
    return Response(serializer.data)
