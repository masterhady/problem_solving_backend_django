from django.http import JsonResponse
from django.conf import settings

def db_status_simple(request):
    try:
        from django.db import connection
        db_config = getattr(settings, 'DATABASES', {}).get('default', {})
        
        connection_ok = False
        connection_error = None
        try:
            if db_config:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    connection_ok = True
            else:
                connection_error = "No default database configuration found"
        except Exception as e:
            connection_ok = False
            connection_error = str(e)
            
        return JsonResponse({
            "db_engine": db_config.get('ENGINE'),
            "db_host": db_config.get('HOST'),
            "db_name": str(db_config.get('NAME')),
            "connection_ok": connection_ok,
            "connection_error": connection_error,
            "use_sqlite": getattr(settings, 'USE_SQLITE', 'Not Set'),
            "debug_mode": settings.DEBUG
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
