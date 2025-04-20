from rest_framework import serializers
from .models import ProxySettings, ProxyLog

class ProxySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxySettings
        fields = ['proxy_enabled', 'blacklist_enabled', 'logs_enabled']

class ProxyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxyLog
        fields = '__all__'
