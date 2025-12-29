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
            
        import os
        return JsonResponse({
            "db_engine": str(db_config.get('ENGINE')),
            "db_host_config": str(db_config.get('HOST')),
            "db_name": str(db_config.get('NAME')),
            "connection_ok": str(connection_ok),
            "connection_error": str(connection_error),
            "env_db_host_present": str('DB_HOST' in os.environ),
            "env_use_sqlite": str(os.environ.get('USE_SQLITE')),
            "use_sqlite_config": str(getattr(settings, 'USE_SQLITE', 'Not Set')),
            "debug_mode": str(settings.DEBUG)
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
