import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProxyLogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("proxy_logs", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("proxy_logs", self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_log(self, event):
        log = event['log']
        await self.send(text_data=json.dumps(log))

