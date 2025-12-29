from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.conf import settings
from django.db import connection

class DbStatusView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        db_config = getattr(settings, 'DATABASES', {}).get('default', {})
        db_info = {
            "engine": db_config.get('ENGINE'),
            "host": db_config.get('HOST'),
            "name": db_config.get('NAME'),
            "user": db_config.get('USER'),
        }
        
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
            
        return Response({
            "db_info": db_info,
            "connection_ok": connection_ok,
            "connection_error": connection_error,
            "use_sqlite": getattr(settings, 'USE_SQLITE', 'Not Set'),
            "debug_mode": settings.DEBUG
        })
