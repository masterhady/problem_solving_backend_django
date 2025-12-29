from django.http import JsonResponse
from django.conf import settings

def health_check(request):
    import os
    from django.conf import settings
    db_engine = settings.DATABASES['default']['ENGINE']
    
    # Masked environment variables for debugging
    env_vars = {k: (v[:3] + "..." if len(v) > 3 else "***") for k, v in os.environ.items() if "DB" in k or "SQLITE" in k}
    
    return JsonResponse({
        "status": "ok", 
        "message": "Backend is running",
        "database": db_engine,
        "env_debug": env_vars
    })
