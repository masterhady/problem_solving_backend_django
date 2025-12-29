from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.conf import settings
from django.db import connection

class DbStatusView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        db_info = {
            "engine": settings.DATABASES['default']['ENGINE'],
            "host": settings.DATABASES['default'].get('HOST'),
            "name": settings.DATABASES['default'].get('NAME'),
            "user": settings.DATABASES['default'].get('USER'),
        }
        
        connection_error = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                connection_ok = True
        except Exception as e:
            connection_ok = False
            connection_error = str(e)
            
        return Response({
            "db_info": db_info,
            "connection_ok": connection_ok,
            "connection_error": connection_error if not connection_ok else None,
            "use_sqlite": getattr(settings, 'USE_SQLITE', 'Not Set')
        })
