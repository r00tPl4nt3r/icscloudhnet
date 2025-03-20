### How to install


    git clone https://github.com/r00tPl4nt3r/icscloudhnet
    sh icscloudhnet/install.sh
    cd icscloudhnet/deployments/FT9V/docker/
    docker compose

    Open http://localhost:1880/ui

Once the deployment is installed the UI will be available:

![UserInterface](/doc/images/ui.png "UI")

Also you can test the MQTT broker working by opening any MQTT client and querying your local interface ip address:

![UserInterface](/doc/images/mqtt_client.png "UI")

# Deployments

## FischerTechnik 9v

- MQTT broker
- MQTT producer/receiver
- UI Interface


##  FischerTechnik 24v 

- MQTT Broker
- HMI (NodeRED)(client with support for OPCUA and MQTT)
- MQTT producer/receiver
- PLC (OPCUA Server)

### How to install

    gh repo clone r00tPl4nt3r/icscloudhnet
    sh icscloudhnet/install.sh
    cd icscloudhnet/deployments/FT24V/docker/
    docker compose




