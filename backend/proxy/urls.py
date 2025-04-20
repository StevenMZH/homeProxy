from django.urls import path
from .views import ProxySettingsView, ProxyLogListView

urlpatterns = [
    path('settings/', ProxySettingsView.as_view(), name='proxy-settings'),
    path('logs/', ProxyLogListView.as_view(), name='proxy_log_list'),
]
