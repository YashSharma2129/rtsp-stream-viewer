import base64
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            encoded_url = self.scope['url_route']['kwargs']['stream_path']
            
            # Add back padding if needed
            padding = len(encoded_url) % 4
            if padding:
                encoded_url += '=' * (4 - padding)
            
            # Convert URL-safe base64 back to original URL
            base64_str = encoded_url.replace('-', '+').replace('_', '/')
            rtsp_url = base64.b64decode(base64_str).decode('utf-8')
            
            await self.accept()
            # Send connection success message
            await self.send(text_data=json.dumps({
                'status': 'connected',
                'message': 'Successfully connected to WebSocket'
            }))
            
        except Exception as e:
            await self.accept()
            await self.send(text_data=json.dumps({
                'status': 'error',
                'message': str(e)
            }))
            await self.close()
