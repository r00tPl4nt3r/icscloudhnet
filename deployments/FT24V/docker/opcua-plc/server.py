from opcua import ua, Server
import time, random
import logging

logging.basicConfig(level=logging.DEBUG)


# Create an OPC UA server instance
server = Server()
# Define the endpoint URL for the server
url = "opc.tcp://0.0.0.0:4840"
server.set_endpoint(url)




# Create a new address space
address_space = server.register_namespace("MyNamespace")

# Create a folder node to organize the nodes
folder = server.get_objects_node().add_object(address_space, "MyFolder")

# Create a DeviceSet node to organize the nodes
plc = server.get_objects_node().add_object(address_space, "PLC")

# Add nodes to the address space
individual_weight_node = folder.add_variable(address_space, "ns=4;s=individual_weight", "Individual Weight")
request_to_collect_node = folder.add_variable(address_space, "ns=4;s=request_to_collect", "Request to Collect")
gtyp_Interface_Dashboard = plc.add_variable(address_space,'ns=3;s="gtyp_Interface_Dashboard"."Subscribe"."State_Order"."s_state"', "State_Order")
plc.a

# Set the nodes as writable
individual_weight_node.set_writable()
request_to_collect_node.set_writable()

# Assign values to the nodes
individual_weight_node.set_value(1500)
request_to_collect_node.set_value(False)
gtyp_Interface_Dashboard.set_value("Test")


# Start the OPC UA server
server.start()
logging.debug("OPC UA server started at", url)

def generate_random_weight():
    
    random_number = random.randint(1500, 3000)  
    return random_number

# Run the server indefinitely
try:
    while True:
        time.sleep(10)
        # if request_to_collect is false set it to true
        if not request_to_collect_node.get_value():
            request_to_collect_node.set_value(True)
        weight = generate_random_weight()
        individual_weight_node.set_value(weight)
        logging.debug(individual_weight_node.get_value())
        # set request_to_collect to false to indicate object is collected 
        request_to_collect_node.set_value(False)
        logging.debug("This is the values %s", request_to_collect_node.get_value())
         
except KeyboardInterrupt:
    server.stop()
    logging.debug("OPC UA server stopped")