from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProxySettings, ProxyLog
from .serializers import ProxyLogSerializer

import socket

# Configuración del socket para comunicarse con el Proxy Server
PROXY_SERVER_SOCKET_PATH = '/tmp/proxy_server.sock'

# Estado en memoria
proxy_state = {
    'proxyActive': False,
    'blacklistEnabled': False,
    'logsEnabled': False,
}

def send_command_to_proxy(command: str) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('127.0.0.1', 9999))
            client_socket.sendall(command.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Respuesta del proxy: {response}")
            return response == "OK"
    except Exception as e:
        print(f"Error al comunicar con el proxy: {e}")
        return False

class ProxyStatusView(APIView):
    def get(self, request):
        return Response(proxy_state, status=status.HTTP_200_OK)

class ProxyControlView(APIView):
    def post(self, request):
        proxy_active = request.data.get('proxyActive')
        blacklist_enabled = request.data.get('blacklistEnabled')
        logs_enabled = request.data.get('logsEnabled')

        if proxy_active is None or blacklist_enabled is None or logs_enabled is None:
            return Response({'error': 'Missing proxyActive, blacklistEnabled, or logsEnabled fields'}, status=status.HTTP_400_BAD_REQUEST)

        success = True

        if proxy_active != proxy_state['proxyActive']:
            command = 'START_PROXY' if proxy_active else 'STOP_PROXY'
            if send_command_to_proxy(command):
                proxy_state['proxyActive'] = proxy_active
            else:
                success = False

        if blacklist_enabled != proxy_state['blacklistEnabled']:
            command = 'ENABLE_BLACKLIST' if blacklist_enabled else 'DISABLE_BLACKLIST'
            if send_command_to_proxy(command):
                proxy_state['blacklistEnabled'] = blacklist_enabled
            else:
                success = False

        if logs_enabled != proxy_state['logsEnabled']:
            command = 'ENABLE_LOG' if logs_enabled else 'DISABLE_LOG'
            if send_command_to_proxy(command):
                proxy_state['logsEnabled'] = logs_enabled
            else:
                success = False

        if not success:
            return Response({'error': 'Proxy server communication failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(proxy_state, status=status.HTTP_200_OK)


class ProxyLogListView(generics.ListCreateAPIView):
    queryset = ProxyLog.objects.all()
    serializer_class = ProxyLogSerializer
