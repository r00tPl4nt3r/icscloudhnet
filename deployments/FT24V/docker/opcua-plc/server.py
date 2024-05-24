from opcua import ua, Server
import time, random

# Create an OPC UA server instance
server = Server()
# Define the endpoint URL for the server
url = "opc.tcp://127.0.0.1:4849"
server.set_endpoint(url)