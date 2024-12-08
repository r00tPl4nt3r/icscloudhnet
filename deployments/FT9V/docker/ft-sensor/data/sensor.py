
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
import json
import time
import random


mqtt_port = 1883
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

while True:
    ibme680 = {
        "aq": 0,
        "gr": 836963.0,
        "h": 0,
        "iaq": 0,
        "p": 0,
        "rh": 0,
        "rt": 0,
        "t": 0,
        "ts": ""
    }

while True:
    try:
        ibme680["aq"] = round(random.gauss(15, 1), 1)
        ibme680["h"] = round(random.gauss(23, 1), 0)
        ibme680["iaq"] = round(random.gauss(133, 3), 0)
        ibme680["p"] = round(random.gauss(980, 10), 1)
        ibme680["rh"] = round(random.gauss(22, 1), 0)
        ibme680["rt"] = round(random.gauss(23, 0.5), 2)
        ibme680["t"] = round(random.gauss(21, 0.5), 0)
        ibme680["ts"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        mqtt_topic = "i/bme680"
        message = json.dumps(ibme680)
        client.publish(mqtt_topic, message)

        time.sleep(60)
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(5)
