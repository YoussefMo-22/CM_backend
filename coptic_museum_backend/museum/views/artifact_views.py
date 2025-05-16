from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Artifact, Artifact3DModel
from ..serializers import ArtifactSerializer, Artifact3DModelSerializer
from django.core.files.storage import default_storage

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

@api_view(['GET', 'POST'])
def artifacts_list_create(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        artifacts = Artifact.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).order_by('-created_at')
        
        paginator = PageNumberPagination()
        result = paginator.paginate_queryset(artifacts, request)
        serializer = ArtifactSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def artifact_detail(request, pk):
    try:
        artifact = Artifact.objects.get(pk=pk)
    except Artifact.DoesNotExist:
        return Response({"error": "Artifact not found"}, status=404)

    if request.method == 'GET':
        serializer = ArtifactSerializer(artifact)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ArtifactSerializer(artifact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        artifact.delete()
        return Response(status=204)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_artifact_image(request):
    image = request.FILES.get('image')
    if not image:
        return Response({"error": "No image provided."}, status=400)
    path = default_storage.save(image.name, image)
    return Response({"message": "Image uploaded successfully", "path": path})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def identify_artifact(request):
    # Placeholder for AI identification logic
    # You can integrate TensorFlow, PyTorch, or a cloud vision API here
    return Response({"result": "Artifact identified: Coptic Cross"}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_3d_models(request):
    models = Artifact3DModel.objects.all()
    serializer = Artifact3DModelSerializer(models, many=True)
    return Response(serializer.data)
