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


    git clone 
    cd deployments/FT9V/docker
    docker build dockerfiles/ -t ft/ft-ui
    docker compose

    Open http://localhost:1880/ui

Once the deployment is installed the UI will be available:

![UserInterface](/doc/images/ui.png "UI")

Also you can test the MQTT broker working by opening any MQTT client and querying your local interface ip address:

![UserInterface](/doc/images/mqtt_client.png "UI")



## TODO - FischerTechnik 24v

- MQTT broker
- MQTT producer/receiver
- UI Interface
- OpenPLC

