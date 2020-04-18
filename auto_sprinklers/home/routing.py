from home.consumers import ws_message, ws_connect, ws_disconnect
#from . import consumers

channel_routing = {
    'websocket.connect': ws_connect,
    'websocket.receive': ws_message,
    'websocket.disconnect': ws_disconnect,
    'websocket.keepalive': ws_message,
}