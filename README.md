# icscloudhnet
Honeynet deployment for cloud environments.

[TOC]

# Architecture

This is the architecture for the solution:

![architecture](/doc/images/architecture.drawio.svg "Architecture")

# Deployments

## FischerTechnik 9v

- MQTT broker
- MQTT producer/receiver
- UI Interface

### How to install


    git clone https://github.com/r00tPl4nt3r/icscloudhnet
    cd icscloudhnet/deployments/FT9V/docker/
    docker build ft-ui/ -t ft/ft-ui
    docker compose

    Open http://localhost:1880/ui

Once the deployment is installed the UI will be available:

![UserInterface](/doc/images/ui.png "UI")

Also you can test the MQTT broker working by opening any MQTT client and querying your local interface ip address:

![UserInterface](/doc/images/mqtt_client.png "UI")

##  FischerTechnik 24v 

- MQTT Broker
- HMI (NodeRED)(client with support for OPCUA and MQTT)
- MQTT producer/receiver
- PLC (OPCUA Server)

### How to install

    gh repo clone r00tPl4nt3r/icscloudhnet
    cd deployments/FT24V/docker
    docker build dockerfiles/ -t ft/ft-ui
    docker compose


## TODO - FischerTechnik 24v (Done)

- MQTT broker (Solved)
- MQTT producer/receiver(Solved)
- UI Interface(Solved)
- OPCUA deployment (Solved)
- OPCUA Collector ((Solved))

## TODO General

- Logging
- Networking
    - Client
    - SErver

- 
