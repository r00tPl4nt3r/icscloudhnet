# Provisioner Docker App

## Overview

This directory contains the Docker setup for the Provisioner application. The Provisioner app is a Flask-based service that handles deployment requests.

## Building the Docker Image

To build the Docker image for the Provisioner app, navigate to this directory and run the following command:

```sh
docker build -t trapnet-provisioner .
```

## Running the Docker Container

To run the Docker container for the Provisioner app, use the following command:

```sh
docker run -p 6900:5000 trapnet-provisioner
```

This will start the Provisioner app and map port 6900 on your host to port 5000 in the container.

## Using Docker Compose

Alternatively, you can use Docker Compose to manage the entire setup, including the Provisioner app. Ensure you are in the root directory where the `docker-compose.yml` file is located and run:

```sh
docker-compose up
```

This will start all the services defined in the `docker-compose.yml` file, including the Provisioner app.

## Endpoints

- `/` - Returns a greeting message.
- `/provisioner` - Accepts POST requests to handle deployment.

### Required JSON Input for `/provisioner`

```json
{
  "deployment_name": "example_deployment",
  "public_ip_address": "192.168.1.1",
  "local_network_address": "192.168.1.0/24",
  "token": "example_token"
}
```

## Environment Variables

- `FLASK_ENV` - Set to `development` for development mode.

## Health Check

The Provisioner service includes a health check that can be configured in the `docker-compose.yml` file.

## License

This project is licensed under the MIT License.
