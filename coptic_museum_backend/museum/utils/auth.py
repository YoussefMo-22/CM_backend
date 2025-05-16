
from django.http import JsonResponse
import os

def require_token(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.headers.get("X-API-Token")
        expected = os.environ.get("DJANGO_SHARED_SECRET")
        if token != expected:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper