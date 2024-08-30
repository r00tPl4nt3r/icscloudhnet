# Script to test multiple functions from an mqtt server for multiple purposes
# Use:
#   python3 mqtt_tester.py <function> <mqtt_ip> [--ssl]
# Example:
#   python3 mqtt_tester.py --connection <mqtt_ip>
#   python3 mqtt_tester.py --publication <mqtt_ip>
#   python3 mqtt_tester.py --subscription <mqtt_ip>

import paho.mqtt.client as mqtt
import sys
import time as sleep
import ssl

if len(sys.argv)<2 or sys.argv[1]=="-h" or sys.argv[1]=="--help":
    print("Usage: python3 mqtt_tester.py <function> <mqtt_ip> [--ssl]")
    print("Example:")
    print("  python3 mqtt_tester.py --connection <mqtt_ip>")
    print("  python3 mqtt_tester.py --publication <mqtt_ip>")
    print("  python3 mqtt_tester.py --subscription <mqtt_ip>")
    print("  python3 mqtt_tester.py --connection <mqtt_ip> --ssl")
    sys.exit()



#define mqtt ip address from argument
mqtt_ip = sys.argv[2]
mqtt_port = 8883
time=100

"resolve mqtt_ip domain"
import socket
try:
    mqtt_ip = socket.gethostbyname(mqtt_ip)
except:
    print("Error: Cannot resolve the mqtt server")
    mqtt_ip = socket.gethostbyaddr(mqtt_ip)
    sys.exit()



if sys.argv[1]=="--connection":

    print("Testing connection to the mqtt server: ", mqtt_ip, " for ", time, " times")

    for i in range(0,time):
        print("Time: ", i+1)


        if len(sys.argv)>3 and sys.argv[3]=="--ssl":
            "Connect to the mqtt broker with ssl"
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            client.username_pw_set("testtest", "Testtest1")
            client.tls_set(certfile=None,
                        keyfile=None,
                        cert_reqs=ssl.CERT_REQUIRED)
            client.tls_insecure_set(True)
            client.connect(mqtt_ip, mqtt_port, 60)
            client.loop_start()

        
        else:

            "Connect to the mqtt broker"
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            client.connect(mqtt_ip, mqtt_port, 60)
            client.loop_start()

        "Disconnect from the mqtt broker"
        client.loop_stop()
        client.disconnect()


elif sys.argv[1]=="--publication":
    
    print("Testing publishing to the mqtt server: ", mqtt_ip, " for ", time, " times")


    "Connect to the mqtt broker"
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(mqtt_ip, mqtt_port, 60)
    client.loop_start()

    for i in range(0,time):
        print("Time: ", i+1)

        "Publish to the mqtt broker"
        client.publish("test", "test number: "+str(i+1))
        sleep.sleep(1)

    "Disconnect from the mqtt broker"
    client.loop_stop()
    client.disconnect()


elif sys.argv[1]=="--subscription":
    print("Testing subscribing and unsubscribing to the mqtt server: ", mqtt_ip, " for ", time, " times")
    
    "Connect to the mqtt broker"
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(mqtt_ip, mqtt_port, 60)
    client.loop_start()

    for i in range(0,time):
        print("Time: ", i+1)

        "Subscribe to the mqtt broker"
        client.subscribe("test")

        "Unsubscribe from the mqtt broker"
        client.unsubscribe("test")
        sleep.sleep(1)
    
    "Disconnect from the mqtt broker"
    client.loop_stop()
    client.disconnect()


