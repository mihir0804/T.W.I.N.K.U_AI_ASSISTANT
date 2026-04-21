import asyncio
import json
import websockets
import threading

class TwinkuBroadcaster:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.current_state = {"status": "idle", "transcript": ""}
        self.loop = None
        self.on_message_callback = None

    async def register(self, websocket):
        self.clients.add(websocket)
        try:
            await websocket.send(json.dumps(self.current_state))
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if self.on_message_callback:
                        self.on_message_callback(data)
                except Exception as e:
                    print(f"WS Recv Error: {e}")
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)

    async def _async_start(self):
        print(f"🚀 Twinku WebSocket Server running on ws://{self.host}:{self.port}")
        async with websockets.serve(self.register, self.host, self.port):
            await asyncio.Future()  # run forever

    def _start_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._async_start())

    def start(self):
        t = threading.Thread(target=self._start_loop, daemon=True)
        t.start()
        
    def _do_broadcast(self, state):
        if self.clients:
            websockets.broadcast(self.clients, json.dumps(state))

    def broadcast(self, status, transcript="", audioLevel=0):
        self.current_state = {"status": status, "transcript": transcript, "audioLevel": audioLevel}
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(
                asyncio.sleep(0), self.loop # a dummy way to invoke into event loop
            )
            # Actually, websockets.broadcast is not strictly thread safe, but often works.
            # To be safe:
            self.loop.call_soon_threadsafe(self._do_broadcast, self.current_state)
