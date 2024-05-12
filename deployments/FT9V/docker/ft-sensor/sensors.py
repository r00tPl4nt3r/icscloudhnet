
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
import json
from IPython import display
import base64
import time
import random


port = 1883
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("ft-broker", port=port)


data = {}
with open('./data/21.jpg', mode='rb') as file:
    img = file.read()

icamera={ 
    "data" : "data:image/jpeg;base64,"+base64.encodebytes(img).decode('utf-8'),
    "ts" : datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }

client.connect("ft-broker", port=port)
topic = "i/cam"
message= json.dumps(icamera)
client.publish(topic, message)

while True:
    ibme680={"aq" : round(random.gauss(15, 1),1) ,
        "gr" : 836963.0,
        "h" : round(random.gauss(23, 1),0),
        "iaq" : round(random.gauss(133, 3),0),
        "p" : round(random.gauss(980, 10),1),
        "rh" : round(random.gauss(22, 1),0),
        "rt" : round(random.gauss(23, 0.5),2),
        "t" : round(random.gauss(21, 0.5),0),
        "ts" : datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}
    client.connect("ft-broker", port=port)
    topic = "i/bme680"
    message = json.dumps(ibme680)
    client.publish(topic, message)

    time.sleep(60)

