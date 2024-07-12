import csv
from opcua import Client, ua

# Define the OPC UA server
OPC_SERVER = "opc.tcp://192.168.0.1:4840"
# Define the OPC UA server variable to change and value to write
VARTOCHANGE = 'ns=3;s="gtyp_SSC"."di_Pos_Park_Horizontal"'
NEWVALUE = 3001

def main():

    client = Client(OPC_SERVER)
    client.connect()
    client.load_type_definitions()  # load definition of server specific structures/extension objects

    # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
    root = client.get_root_node()
    print("Root node is: ", root)
    objects = client.get_objects_node()
    print("Objects node is: ", objects)

    # Node objects have methods to read and write node attributes as well as browse or populate address space
    print("Children of root are: ", root.get_children())

    variable = client.get_node(VARTOCHANGE)
    print("Variable is: ", variable.get_value())
    'write value to the variable'

    try:
        newvalue = ua.DataValue(ua.Variant(NEWVALUE, ua.VariantType.Int32))
        newvalue.ServerTimestamp = None
        newvalue.SourceTimestamp = None
        variable.set_value(newvalue)
        print("Value written to the variable", VARTOCHANGE," : ", variable.get_value())
    except Exception as e:
        print("Error writing value to the variable: ", e)
    
    client.disconnect()


if __name__ == "__main__":
    main()

