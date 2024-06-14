from opcua import ua, Client

# Define the server endpoint URL
url = "opc.tcp://192.168.0.110"

# Create a client and connect to the server
client = Client(url)
client.connect()
print("Connected to OPC UA server")

while True:
    individual_weight_node = client.get_node("ns=2;i=2")
    request_to_collect_node = client.get_node("ns=2;i=3")

    # Read the value of the request_to_collect_node
    request_to_collect_value = request_to_collect_node.get_value()

    # Check if request_to_collect_node value is True
    if request_to_collect_value:
        # Read the value of the individual_weight_node
        weight_value = individual_weight_node.get_value()
        print("Weight:", weight_value)
    else:
        print("Request to collect is False, weight collection not requested.")