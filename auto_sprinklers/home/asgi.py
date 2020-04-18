import os
from channels.layers import get_channel_layer
#import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home.settings")
#channel_layer = channels.asgi.get_channel_layer()
channel_layer = get_channel_layer()