import socket
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class Index(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        return Response({
            'app': 'shitter'
        })


class HealthCheck(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        return Response({
            'alive': True,
            'host': socket.gethostname(),
            'version': getattr(settings, 'VERSION'),
            'ip': request.ip,
        })


index = Index.as_view()
health_check = HealthCheck.as_view()
