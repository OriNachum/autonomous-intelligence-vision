import asyncio
import websockets

if __name__ == "__main__":
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)

from services.get_current_ip import get_ethernet_ip

SECRET_KEY = "your_secret_key"

# Add SSL, add bruteforce attack support
async def websocket_handler(websocket, path):
    try:
        async for message in websocket:
            if not message.startswith(SECRET_KEY):
                raise ValueError("invalid key or token")
            
            print(f"Received {message}")
            response = f"Server: Message resceived from {message.split(':')[1].split(' ')[0]}"
            await websocket.send(response)
    except ValueError:
        print("Secret error")
        await websocket.close()

current_ip = get_ethernet_ip()
start_server = websockets.serve(websocket_handler, current_ip, 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
