# Trapnet
Honeynet deployment for cloud environments.

[TOC]

# Architecture

This is the architecture for the solution:

![architecture](doc/images/design.drawio(2).png "Architecture")


# How to Start.

This is the deployment list. You need at least an on-site connector and one cloud deployment. For scaling, multiple deployments and centralized administration you will need the Provisioning Service (provisioning).

![deployments](/doc/images/architecture.png "Deployments")

1. [Install the Provisioner](/deployments/Provisioner/README.md)
2. [Install the on-site connector.](/doc/cloud.copy.md)
3. [Install the cloud deployment.](/doc/interface.md)
4. [Install a deployment in the cloud host.](deployments/README.md)


If you want to install the honeynet go directly to [Deployments](/deployments/README.md).


