from opcua import ua, Server
import time, random
import logging
import csv

logging.basicConfig(level=logging.WARN)


# Create an OPC UA server instance
server = Server()
# Define the endpoint URL for the server
url = "opc.tcp://0.0.0.0:4840"
server.set_endpoint(url)


# Create a new address space
address_space = server.register_namespace("Fischertechnik")

# Create a PLC node to organize the nodes
plc = server.get_objects_node().add_object(address_space, "PLC")


# Open the file
with open('./data/file.csv', 'r') as file:
    # Create a CSV reader
    reader = csv.reader(file, delimiter='|')
    
    # Initialize an empty list to store the tuples
    tuple_list = []
    
    # Iterate over each row in the file
    for row in reader:
        # Create a tuple from the row values
        tuple_row = (row[0], row[1], row[2], row[3], row[4])
        
        # Append the tuple to the list
        tuple_list.append(tuple_row)
        opcua_variable = plc.add_variable(address_space,row[0],row[3])
        opcua_variable.set_writable()
        opcua_variable.set_value(row[4])
        


# Start the OPC UA server
server.start()
logging.debug("OPC UA server started at", url)

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    server.stop()
    logging.debug("OPC UA server stopped")