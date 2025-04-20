from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProxySettings, ProxyLog
from .serializers import ProxySettingsSerializer, ProxyLogSerializer

class ProxySettingsView(APIView):
    def get(self, request):
        settings, created = ProxySettings.objects.get_or_create(id=1)
        serializer = ProxySettingsSerializer(settings)
        return Response(serializer.data)

    def post(self, request):
        settings, created = ProxySettings.objects.get_or_create(id=1)
        serializer = ProxySettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProxyLogListView(generics.ListCreateAPIView):
    queryset = ProxyLog.objects.all()
    serializer_class = ProxyLogSerializer
