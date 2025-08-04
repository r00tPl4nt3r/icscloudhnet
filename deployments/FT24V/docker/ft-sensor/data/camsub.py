from datetime import datetime, timezone
import json
from IPython import display
import base64
import time
import paho.mqtt.client as mqtt
import logging

logger = logging.getLogger("ft-sensor")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

x = y = 1
min = 0
max = 3

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    logger.info(f"Connected with result code {reason_code}")
    client.subscribe("o/ptu")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global x, y
    logger.info(f"Received from sbscription topic: {msg.topic} message: {msg.payload}")

    jsonmsg = json.loads(msg.payload.decode())

    if jsonmsg["cmd"] == "relmove_left": x = (x - 1) % max; time.sleep(2)
    if jsonmsg["cmd"] == "relmove_right": x = (x + 1) % max; time.sleep(2)
    if jsonmsg["cmd"] == "relmove_down": y = (y + 1) % max; time.sleep(2)
    if jsonmsg["cmd"] == "relmove_up": y = (y - 1) % max; time.sleep(2)
    if jsonmsg["cmd"] == "start_pan": x = min; time.sleep(3)
    if jsonmsg["cmd"] == "end_pan": x = max - 1; time.sleep(3)
    if jsonmsg["cmd"] == "start_tilt": y = max - 1; time.sleep(3)
    if jsonmsg["cmd"] == "end_tilt": y = min; time.sleep(3)
    if jsonmsg["cmd"] == "home": x = y = 1; time.sleep(5)
    if jsonmsg["cmd"] == "stop": True  # This line has no effect; consider revising it.

    data = {}
    with open(f'./data/img/{x}{y}.jpg', mode='rb') as file:
        img = file.read()

    icamera = {
        "data": "data:image/jpeg;base64," + base64.encodebytes(img).decode('utf-8'),
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }

    topic = "i/cam"
    message = json.dumps(icamera)
    client.publish(topic, message)
    logger.info(f"Published message to topic {topic}")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("ft-broker-plc", 1883, 60)
mqttc.loop_forever()
