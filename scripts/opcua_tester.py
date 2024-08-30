# Script to test multiple functions from an opcua server for multiple purposes
# Use:
#   python3 opcua_tester.py <function> <opcua_ip> [--ssl]
# Example:
#   python3 opcua_tester.py --connection <opcua_ip> [number] [--ssl]
#   python3 opcua_tester.py --request <opcua_ip> [number] [--ssl]
#   python3 opcua_tester.py --write <opcua_ip> [number] [--ssl]

import sys
from opcua import Client, ua

FIXED_VARIABLE = "ns=3;s=\"gtyp_SSC\".\"di_Pos_Park_Horizontal\""

def main():
        
    if len(sys.argv) < 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("Error: Missing arguments")
        print("Usage: python3 opcua_tester.py <function> <opcua_ip> [--ssl]")
        print("Example:")
        print("  python3 opcua_tester.py --connection <opcua_ip>")
        print("  python3 opcua_tester.py --request <opcua_ip>")
        print("  python3 opcua_tester.py --write <opcua_ip>")
        

    if sys.argv[1]=="--connection":
        # Define the OPC UA server
        OPC_SERVER = sys.argv[2]

        if len(sys.argv) >3 and type(sys.argv[3])==int:
            number = sys.argv[3]
            print("Number of connections: ", number)
        else:
            number = 100

        print("OPC Server: ", OPC_SERVER)
        print("Testing connection to the OPCUA server: ", OPC_SERVER, " for ", number, " times")


        for i in range(0,number):
            
            if "--ssl" in sys.argv:
                # Connect to the opcua server with ssl
                client = Client(OPC_SERVER, security_mode=ua.MessageSecurityMode.SignAndEncrypt, security_policy=ua.SecurityPolicy.Basic256Sha256)
            
            else:
                client = Client(OPC_SERVER)
        
            client.connect()
            print("Connection ", i+1, " established")
            client.disconnect()
            print("Connection ", i+1, " closed")

    if sys.argv[1]=="--request":
        # Define the OPC UA server
        OPC_SERVER = sys.argv[2]
        # Define the OPC UA server variable to change and value to write
        VARTOCHANGE = FIXED_VARIABLE

        if len(sys.argv) >3 and type(int(sys.argv[3]))==int:
            number = int(sys.argv[3])
            print("Number of connections: ", number)
        else:
            number = 100

        client = Client(OPC_SERVER)
        client.connect()


        for i in range(0,number):
            value = client.get_node(VARTOCHANGE)
            'print value'
            print("Request number: ", i+1," - Value: ", value.get_value())

            #print("Request number: ", i+1)
        
        client.disconnect()


    if sys.argv[1]=="--write":
        # Define the OPC UA server
        OPC_SERVER = sys.argv[2]
        # Define the OPC UA server variable to change and value to write
        VARTOCHANGE = FIXED_VARIABLE
        NEWVALUE = 3001

        if len(sys.argv) >3 and type(int(sys.argv[3]))==int:
            number = int(sys.argv[3])
            print("Number of connections: ", number)
        else:
            number = 100

        client = Client(OPC_SERVER)
        client.connect()

        for i in range(0,number):
            variable = client.get_node(VARTOCHANGE)
            newvalue = ua.DataValue(ua.Variant(NEWVALUE, ua.VariantType.Int32))
            variable.set_value(newvalue)
            print("Request number: ", i+1)

        client.disconnect()
    

if __name__ == "__main__":
    main()

    