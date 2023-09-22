# ably.py
import time
from umqtt.simple import MQTTClient
import badger2040
from badger2040 import WIDTH
import urequests as requests
import ujson

# BAD WORDS API CONFIG
BAD_WORDS_SERVER='https://api.apilayer.com/bad_words'
BAD_WORDS_API_KEY='<YOUR_BAD_WORDS_API_KEY>'

# ABLY CONFIG
ABLY_SERVER ="mqtt.ably.io"
ABLY_CLIENT_ID = f'raspberry-sub-{time.time_ns()}'
ABLY_API_KEY = "<YOUR_ABLY_API_KEY>"
password = "" # No password needed.
ABLY_CHANNEL = "<YOUR_ABLY_CHANNEL>"

# SCREEN CONFIG
TEXT_SIZE = 1
LINE_HEIGHT = 16
SCREEN_WIDTH = WIDTH -15

display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(2)
display.connect()

def checkMessage(msg):
    print('Checking message quality for "%s"' % (msg))
    request_url = BAD_WORDS_SERVER
    res = requests.post(request_url, data=msg, headers={'apikey': BAD_WORDS_API_KEY}).json()
    print('Message may have been censored with: "%s"' % (res['censored_content']))
    print("Message quality checked")
    
    return res


def sub(channel, msg, check=True):
    print('Message received: "%s" in channel "%s"' % (msg, ABLY_CHANNEL))
    
    if check:
        censoredMessage = checkMessage(msg)
        msg = censoredMessage['censored_content']

    y = 35 + int(LINE_HEIGHT / 2)

    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    display.rectangle(0, 0, WIDTH, 20)
    display.text(msg, 5, y, SCREEN_WIDTH)
    display.update()
    
client = MQTTClient(ABLY_CLIENT_ID, ABLY_SERVER, 1883, ABLY_API_KEY, password)
client.set_callback(sub)

# Default message to display.
sub(ABLY_CHANNEL, "Hello, welcome to the Ably Subscriber Badge.", False)

client.connect()
print('Connected to MQTT Ably "%s"' % (ABLY_SERVER))

client.subscribe(ABLY_CHANNEL)

while True:
    display.keepalive()
    if True:
        client.wait_msg()
        time.sleep(20)
    else:
        client.check_msg()
        time.sleep(20)