# backend/proxy/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/logs/', consumers.ProxyLogConsumer.as_asgi()),
]
