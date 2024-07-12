# Script to write a value to an OPC UA server variable using the OPC UA Python library.
# Use:
#   python <server> <variable> <value>
# Example: 
#   python3 opc_writer.py "opc.tcp://192.168.0.1:4840" 'ns=3;s=\"gtyp_SSC\".\"di_Pos_Park_Horizontal\"' 3001
# keep in mind that the variable to write must be of the correct data type.
# also the variable must be writable and quoted correctly.

import sys
from opcua import Client, ua

#Values to be used in the script if not provided as arguments. Use --valuesfromscript to use these values
FIXED_SERVER = "opc.tcp://192.168.0.1:4840"
FIXED_VARIABLE = "ns=3;s=\"gtyp_SSC\".\"di_Pos_Park_Horizontal\""
FIXED_VALUE = 3001

if len(sys.argv) < 1:
    print("Error: Missing arguments")
    print("Usage: python3 opc_writer.py <server> <variable> <value>")
    print("Example:")
    print('python3 opc_writer.py \"opc.tcp://192.168.0.1:4840\" \'ns=3;s=\\\"gtyp_SSC\\\".\\\"di_Pos_Park_Horizontal\\\"\' 3001')
    print("Use --valuesfromscript to use the values defined in the script")
    print("Use -h for help")
    sys.exit()
elif sys.argv[1] == "-h":
    print("Usage: python3 opc_writer.py <server> <variable> <value>")
    print('python3 opc_writer.py \"opc.tcp://192.168.0.1:4840\" \'ns=3;s=\\\"gtyp_SSC\\\".\\\"di_Pos_Park_Horizontal\\\"\' 3001')
    print("Use --valuesfromscript to use the values defined in the script")
    sys.exit()
elif sys.argv[1] == "--valuesfromscript":
    'Define the values here to be used in the script if not provided as arguments'
    # Define the OPC UA server
    OPC_SERVER = FIXED_SERVER
    # Define the OPC UA server variable to change and value to write
    VARTOCHANGE = FIXED_VARIABLE
    NEWVALUE = FIXED_VALUE
else:
    # Define the OPC UA server
    OPC_SERVER = sys.argv[1]
    # Define the OPC UA server variable to change and value to write
    VARTOCHANGE = str(sys.argv[2])
    NEWVALUE = int(sys.argv[3])



def main():

    print("OPC Server: ", OPC_SERVER)
    print("Variable to change: ", VARTOCHANGE)
    print("New value: ", NEWVALUE)

    client = Client(OPC_SERVER)
    client.connect()
    client.load_type_definitions()  # load definition of server specific structures/extension objects

    # Print the root and objects node. Just in case you want to see them.
    root = client.get_root_node()
    print("Root node is: ", root)
    objects = client.get_objects_node()
    print("Objects node is: ", objects)

    variable = client.get_node(VARTOCHANGE)
    print("Variable is: ", variable.get_value())
    
    # Write value to the variable
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

