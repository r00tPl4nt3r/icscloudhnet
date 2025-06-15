import asyncio
import logging
import csv
import sys
from asyncua import ua, Server

csv.field_size_limit(sys.maxsize)

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("asyncua_server")


async def main():
    # Create an OPC UA server instance
    server = Server()
    url = "opc.tcp://0.0.0.0:4840"
    await server.init()
    server.set_endpoint(url)
    server.set_server_name("SIEMENS OPC UA Server")
    server.set_application_uri("urn:Siemens:opcua:server")

    logger.info("OPC UA server started at %s", url)
    #logger.info("Server application URI: %s", server.application_uri)

    # Create a new address space
    ns_two = await server.register_namespace("two")
    ns_three = await server.register_namespace("three")  # used for nodes

    # Create a PLC node
    plc = await server.nodes.objects.add_object(ns_three, "PLC")

    await plc.write_attribute(
    ua.AttributeIds.DisplayName,
    ua.DataValue(ua.LocalizedText("PLC"))
    )

    await plc.write_attribute(
    ua.AttributeIds.Description,
    ua.DataValue(ua.LocalizedText("PLC node"))
    )


    logger.info("PLC node created with NodeId: %s", plc.nodeid)

    gtyp_VGR = await plc.add_object(ns_three, "gtyp_VGR")
    gtyp_Setup = await plc.add_object(ns_three, "gtyp_Setup")
    gtyp_HBW = await plc.add_object(ns_three, "gtyp_HBW")
    gtyp_SSC = await plc.add_object(ns_three, "gtyp_SSC")

    # Open the file and read node definitions
    with open('./data/opcua_tree.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip header
        for row in reader:
            if row[10] == "NodeClass.Variable" and "gtyp" in row[0]:
                try:
                    s_nodeid = row[0].split(";s=")[1]
                    datatype = "ua." + row[4].split("type:")[1].split(")")[0]
                    if datatype in ["ua.VariantType.Int16", "ua.VariantType.Int32", "ua.VariantType.Int64"]:
                        value = int(row[4].split("val:")[1].split(",")[0])
                    else:
                        continue
                except Exception as e:
                    logger.error("Error processing row: %s", row)
                    logger.error("Error details: %s", e)
                    continue

                node_parent = None
                if "gtyp_VGR" in row[0]:
                    node_parent = gtyp_VGR
                elif "gtyp_Setup" in row[0]:
                    node_parent = gtyp_Setup
                elif "gtyp_HBW" in row[0]:
                    node_parent = gtyp_HBW
                elif "gtyp_SSC" in row[0]:
                    node_parent = gtyp_SSC

                if node_parent:
                    try:
                        variant_type = eval(datatype)
                        variable = await node_parent.add_variable(
                            ua.NodeId(s_nodeid, ns_three), row[3], value, variant_type
                        )
                        await variable.set_writable()
                        await variable.set_value_rank(-1)
                    except Exception as e:
                        logger.error("Error creating variable from row: %s", row)
                        logger.error("Error details: %s", e)

    async with server:
        while True:
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
