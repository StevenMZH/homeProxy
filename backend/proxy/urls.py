from django.urls import path
from .views import ProxyStatusView, ProxyControlView, ProxyLogView

urlpatterns = [
    path('status/', ProxyStatusView.as_view(), name='proxy-status'),
    path('control/', ProxyControlView.as_view(), name='proxy-control'),
    path('logs/', ProxyLogView.as_view(), name='proxy_logs'),
]
