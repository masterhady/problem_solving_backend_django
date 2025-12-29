from django.http import JsonResponse
from django.conf import settings

def health_check(request):
    db_engine = settings.DATABASES['default']['ENGINE']
    return JsonResponse({
        "status": "ok", 
        "message": "Backend is running",
        "database": db_engine
    })
