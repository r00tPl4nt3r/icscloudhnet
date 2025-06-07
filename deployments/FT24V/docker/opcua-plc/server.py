from opcua import ua, Server
from opcua import Node
import time, random, csv, sys
import logging

csv.field_size_limit(sys.maxsize)
logging.basicConfig(level=logging.WARN)


# Create an OPC UA server instance
server = Server()
# Define the endpoint URL for the server
url = "opc.tcp://0.0.0.0:4840"
server.set_endpoint(url)
server.set_server_name("SIEMENS OPC UA Server")
server.description = ua.ApplicationDescription()  
server.description.application_uri = "urn:Siemens:opcua:server"
server.set_application_uri("urn:Siemens:opcua:server")
print("Server started at {}".format(url))
print("Server application URI: {}".format(server.get_application_uri()))  

##0:Root,0:Objects,0:Server,0:Namespaces,0:http://opcfoundation.org/UA/

# Create a new address space
address_space = server.register_namespace("two")
address_space = server.register_namespace("three")

# Create a PLC node to organize the nodes
plc = server.get_objects_node().add_object(address_space, "PLC")
#Set nodeid as a string
plc.set_attribute(ua.AttributeIds.DisplayName, ua.DataValue(ua.LocalizedText("PLC")))
plc.set_attribute(ua.AttributeIds.Description, ua.DataValue(ua.LocalizedText("PLC node")))
print(plc.nodeid)
gtyp_VGR = plc.add_object(address_space, "gtyp_VGR")
gtyp_Setup = plc.add_object(address_space, "gtyp_Setup")
gtyp_HBW = plc.add_object(address_space, "gtyp_HBW")
gtyp_SSC = plc.add_object(address_space, "gtyp_SSC")


# Open the file
with open('./data/opcua_tree.csv', 'r') as file:
    # Create a CSV reader
    reader = csv.reader(file, delimiter=';')
    # Skip the header
    next(reader)
    # Iterate over the rows (10 first lines)

    i=0
    for row in reader:
        if row[10] == "NodeClass.Variable" and "gtyp" in row[0]:
            #print(row)
            try:
                s_nodeid= row[0].split(";s=")[1]
                datatype = "ua." + row[4].split("type:")[1].split(")")[0]
                if datatype == "ua.VariantType.Int16" or datatype == "ua.VariantType.Int32" or datatype == "ua.VariantType.Int64":
                    value = int(row[4].split("val:")[1].split(",")[0])
            except Exception as e:
                print(row)
                print("error:", e)
                continue
            if "gtyp_VGR" in row[0]:
                try:
                    # Add a variable to the PLC node
                    opcuavar = gtyp_VGR.add_variable(ua.NodeId(s_nodeid,3), row[3], value, eval(datatype))
                    opcuavar.set_writable()
                except:
                    print(row)
                    print("error:", e)
            if "gtyp_Setup" in row[0]:  
                try:
                    # Add a variable to the PLC node
                    opcuavar = gtyp_Setup.add_variable(ua.NodeId(s_nodeid,3), row[3], value, eval(datatype))    
                    opcuavar.set_writable()
                except:
                    print(row)
                    print("error:", e)
            if "gtyp_HBW" in row[0]:
                try:
                    # Add a variable to the PLC node
                    opcuavar = gtyp_HBW.add_variable(ua.NodeId(s_nodeid,3), row[3], value, eval(datatype))
                    opcuavar.set_writable() 
                except:
                    print(row)
                    print("error:", e)
            if "gtyp_SSC" in row[0]:
                try:
                    # Add a variable to the PLC node
                    opcuavar = gtyp_SSC.add_variable(ua.NodeId(s_nodeid,3), row[3], value, eval(datatype))
                    opcuavar.set_writable()
                except:
                    print(row)
                    print("error:", e)

# Run the server indefinitely
server.start()
server.set_application_uri("urn:Siemens:opcua:server")
logging.info("OPC UA server Started")

try:
    while True:
        time.sleep(10)

         
except KeyboardInterrupt:
    server.stop()
    logging.debug("OPC UA server stopped")