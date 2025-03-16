# WireGuard Keychain Service

This is a simple Flask application that generates WireGuard key pairs and returns them as a JSON response. The application is containerized using Docker.

## Prerequisites

- Docker
- Docker Compose (optional)

## Getting Started

### Build the Docker Image

To build the Docker image, navigate to the directory containing the `Dockerfile` and run the following command:

```sh
docker build -t trapnet/wg .
```

### Run the Docker Container

To run the Docker container, use the following command:

```sh
docker run -p 5000:5000 trapnet/wg
```

The application will be accessible at `http://localhost:5000`.

## API Endpoints

### `GET /`

Returns a simple greeting message.

### `POST /keychain`

Generates a WireGuard key pair and returns it as a JSON response.

#### Example Response

```json
{
    "private_key": "your_private_key",
    "public_key": "your_public_key"
}
```

## Development

### Running Locally

To run the application locally without Docker, ensure you have Python 3.9 and the required dependencies installed. You can install the dependencies using:

```sh
pip install -r requirements.txt
```

Then, run the application with:

```sh
python app.py
```

### Docker Compose

You can also use Docker Compose to manage the application. Create a `docker-compose.yml` file with the following content:

```yaml
version: '3'
services:
  wg-keychain-service:
    build: .
    ports:
      - "5000:5000"
```

Then, run the following command to start the service:

```sh
docker-compose up
```

## License

This project is licensed under the MIT License.