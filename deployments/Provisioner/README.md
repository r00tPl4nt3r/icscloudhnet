# Provisioner Deployment

This document provides instructions and information about the Provisioner deployment in the Trapnet project.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview
The Provisioner is responsible for managing and automating the deployment of resources within the Trapnet project. This includes provisioning infrastructure, deploying applications, and ensuring that all components are correctly configured.

## Prerequisites
Before deploying the Provisioner, ensure you have the following prerequisites:
- [ ] Docker installed
- [ ] Access to the Trapnet repository

## Installation
To install the Provisioner, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/r00tPl4nt3r/trapnet
    cd trapnet/deployments/Provisioner/docker
    ```

2. Build all the images locally.

    ```sh
    docker build -t trapnet-ca ./ca/
    docker build -t trapnet-api ./flask/
    docker build -t trapnet-provisioner ./provisioner/
    docker build -t trapnet-wg ./wg/
    ```
    

   
2. Build and run the Docker containers using `docker-compose`:
    ```sh
    docker-compose up -d
    ```

## Configuration
Configuration options for the Provisioner can be set through environment variables or command-line arguments. Customize the settings according to your environment and requirements.

## Usage
To use the Provisioner, download the certificates in the `client/certs` folder. The certificates are required to securely manage the honeynet. Once you have deployed the Provisioner, you can get the configurations for the interface and cloud/fog host that will allow you to run the deployments. For more information, refer to the [README.md](../../../../README.md) in the root folder.

The following custom fields to be filled:

- `deployment_name`: The name of the deployment.
- `public_ip_address`: The public IP address associated with the deployment.
- `token`: The authentication token required for accessing the deployment.
- `local_network_address`: The local network address for the deployment.

Please ensure to replace these placeholders with the appropriate values before using the deployment script:

```
curl --cert deployments/Provisioner/docker/client/certs/client.crt --key deployments/Provisioner/docker/client/certs/client.key --cacert deployments/Provisioner/docker/client/certs/ca.crt -X POST https://{apiserver}/provisioner -H 'Content-type:application/json' -d ' { "deployment_name": "FT9V", "public_ip_address": "{public_network_address}s",  "token": "{nonce}'",  "local_network_address":"{local_network_address}}" } ' | jq
```





## Troubleshooting
If you encounter issues during deployment, check the logs for more information:
```sh
docker logs provisioner
```
