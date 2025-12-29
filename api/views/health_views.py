from django.http import JsonResponse
from django.conf import settings

def health_check(request):
    return JsonResponse({
        "status": "ok", 
        "message": "Backend is running"
    })
