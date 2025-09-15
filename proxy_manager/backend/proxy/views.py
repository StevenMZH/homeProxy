from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProxySettings, ProxyLog
from .serializers import ProxyLogSerializer
from datetime import datetime

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import socket
from pathlib import Path
import environ
import os


# import .env
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Configuración del socket para comunicarse con el Proxy Server
PROXY_SERVER_SOCKET_PATH = '/tmp/proxy_server.sock'

# Init States
proxy_state = {
    'proxyActive': True,
    'blacklistEnabled': True,
    'logsEnabled': True,
}

def sendCommand_to_proxy(command: str) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(( '127.0.0.1' , 9999))
            client_socket.sendall(command.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"[Proxy Server] Response: {response}")
            return response == "OK"
        
    except Exception as e:
        print(f"[Backend] Error Sending Proxy settings to the server, via socket: {e}")
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
            if sendCommand_to_proxy(command):
                proxy_state['proxyActive'] = proxy_active
            else:
                success = False

        if blacklist_enabled != proxy_state['blacklistEnabled']:
            command = 'ENABLE_BLACKLIST' if blacklist_enabled else 'DISABLE_BLACKLIST'
            if sendCommand_to_proxy(command):
                proxy_state['blacklistEnabled'] = blacklist_enabled
            else:
                success = False

        if logs_enabled != proxy_state['logsEnabled']:
            command = 'ENABLE_LOG' if logs_enabled else 'DISABLE_LOG'
            if sendCommand_to_proxy(command):
                proxy_state['logsEnabled'] = logs_enabled
            else:
                success = False

        if not success:
            return Response({'error': 'Proxy server communication failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(proxy_state, status=status.HTTP_200_OK)


def send_log_to_websocket(log_data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'logs_group',  # El nombre del grupo que se conecta al WebSocket
        {
            'type': 'send_log',  # Esto llama al método 'send_log' en el consumer
            'log': log_data,
        }
    )

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class ProxyLogView(APIView):
    def post(self, request):
        data = request.data
        try:
            timestamp = datetime.fromisoformat(data.get('timestamp'))
            log = ProxyLog.objects.create(
                timestamp=timestamp,
                client_ip=data.get('client_ip', '0.0.0.0'),
                target_host=data.get('target_host', ''),
                target_ip=data.get('target_ip', '0.0.0.0'),
                status=data.get('status', ''),
                request_data=data.get('request_data', '')
            )

            # Serializar y enviar por WebSocket
            serializer = ProxyLogSerializer(log)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "proxy_logs",
                {
                    "type": "send_log",
                    "log": serializer.data
                }
            )

            return Response({"message": "Log saved and broadcasted successfully."}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        logs = ProxyLog.objects.all().order_by('-timestamp')
        serializer = ProxyLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        ProxyLog.objects.all().delete()
        return Response({"message": "All logs have been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)