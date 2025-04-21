from django.db import models

class ProxySettings(models.Model):
    proxy_active = models.BooleanField(default=True)
    blacklist_active = models.BooleanField(default=True)
    logging_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Proxy Config: Active={self.proxy_active}, Blacklist={self.blacklist_active}, Logging={self.logging_active}"


class ProxyLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    client_ip = models.GenericIPAddressField()
    
    target_host = models.CharField(max_length=255)
    target_ip = models.GenericIPAddressField()
    
    status = models.CharField(max_length=255)
    request_data = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.client_ip} -> {self.target_host}"
