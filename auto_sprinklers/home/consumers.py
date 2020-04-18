from channels import Group
#from channels import Channel


#class Content:
#    def __init__(self, reply_channel):
#        self.reply_channel = reply_channel
#
#    def send(self, json):
#        Channel(self.reply_channel).send({'content': dumps(json)})

def ws_connect(message):
    print("Someone connected.")
    path = message['path']                       # i.e. /sensor/

    if path == b'/home/':
        print("Adding new user to sensor group")
        Group("home").add(message.reply_channel)                         # Adds user to group for broadcast
        message.reply_channel.send({                                       # Reply to individual directly
           "text": "You are connected to sensor group ",
        })
    else:
        print("Strange connector!!")

def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    print("Received!!" + message['text'])

def ws_disconnect(message):
    print("Someone left us...")
    Group("home").discard(message.reply_channel)
