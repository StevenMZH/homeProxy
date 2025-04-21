from django.urls import path
from .views import ProxyStatusView, ProxyControlView, ProxyLogListView

urlpatterns = [
    path('status/', ProxyStatusView.as_view(), name='proxy-status'),
    path('control/', ProxyControlView.as_view(), name='proxy-control'),
    path('logs/', ProxyLogListView.as_view(), name='proxy_log_list'),
]
