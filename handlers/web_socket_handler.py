import asyncio
import json
import os
import sys
import websockets
from services.get_current_ip import get_ethernet_ip

SECRET_KEY = "your_secret_key"

class WebsocketHandler:
    def __init__(self):
        pass

    async def handle_websocket(self, websocket, path):
        try:
            async for message in websocket:
                if not message.startswith(SECRET_KEY):
                    raise ValueError("invalid key or token")

                print(f"Received {message}")
                if message == f"{SECRET_KEY} what_i_see":
                    await self.emit_what_i_see_event(websocket, objects=["person", "car", "tree"], scene="outdoor", image_payload="base64_encoded_image_string")
                elif message == f"{SECRET_KEY} recognized_object":
                    await self.emit_recognized_object_event(websocket, object_type="person", object_id="12345", object_name="Jane Doe", confidence=0.95, image_payload="base64_encoded_image_string")
                else:
                    response = f"Server: Message received from {message.split(' ')[1]}"
                    await websocket.send(response)

        except ValueError:
            print("Secret error")
            await websocket.close()

    async def emit_what_i_see_event(self, websocket, objects, scene, image_payload):
        what_i_see_event = {
            "event_type": "what_i_see",
            "timestamp": "2023-03-27T14:30:00Z",
            "data": {
                "objects": objects,
                "scene": scene,
                "image_payload": image_payload
            }
        }
        await websocket.send(json.dumps(what_i_see_event))

    async def emit_recognized_object_event(self, websocket, object_type, object_id, object_name, confidence, image_payload):
        recognized_object_event = {
            "event_type": "recognized_object",
            "timestamp": "2023-03-27T14:30:00Z",
            "data": {
                "object_type": object_type,
                "object_id": object_id,
                "object_name": object_name,
                "confidence": confidence,
                "image_payload": image_payload
            }
        }
        await websocket.send(json.dumps(recognized_object_event))

if __name__ == "__main__":
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)

    handler = WebsocketHandler()
    current_ip = get_ethernet_ip()
    start_server = websockets.serve(handler.handle_websocket, current_ip, 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()