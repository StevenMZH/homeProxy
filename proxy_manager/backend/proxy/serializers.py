from rest_framework import serializers
from .models import ProxySettings, ProxyLog

class ProxySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxySettings
        fields = ['proxy_active', 'blacklist_active', 'logging_active']

class ProxyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxyLog
        fields = '__all__'
