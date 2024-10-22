# DDClient API Container

This project packages `ddclient` into a Docker container with a Flask-based API. The container allows you to run `ddclient` and expose an API to get the last update, last status, etc. Additionally, it pings a `healthchecks.io` service with the status every time `ddclient` runs.

## Features

- Runs `ddclient` to update dynamic DNS records.
- Exposes a Flask-based API to get the last update, last status, etc.
- Pings `healthchecks.io` with the status of `ddclient` runs.
- Allows optional overwriting of the default `ddclient.conf` file by mounting a custom configuration file.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Build the Docker Image

To build the Docker image, run the following command:

```sh
docker build -t ddclient-api-container .
```

### Run the Docker Container

#### Run with Default Configuration

To run the container with the default ddclient.conf configuration, use the following command:

```bash
docker run -d -p 5000:5000 --name ddclient-api \
    -e HEALTHCHECKS_URL=https://hc-ping.com \
    -e HEALTHCHECKS_ID=YOUR-UNIQUE-ID \
    ddclient-api-container
```

Replace `YOUR-UNIQUE-ID` with your actual `healthchecks.io` unique ID.

#### Run with Custom Configuration

To run the container with a custom ddclient.conf configuration, use the following command:

```bash
docker run -d -p 5000:5000 --name ddclient-api \
    -e HEALTHCHECKS_URL=https://hc-ping.com \
    -e HEALTHCHECKS_ID=YOUR-UNIQUE-ID \
    -v /path/to/your/local/ddclient.conf:/etc/ddclient/ddclient.conf \
    ddclient-api-container
```

Replace `/path/to/your/local/ddclient.conf` with the actual path to your custom `ddclient.conf` file on your local machine.

#### Run with Docker Compose

You can also run the project using Docker Compose. Create a `docker-compose.yml` file with the following content:

```yaml
version: "3.8"

services:
  ddclient-api:
    image: your-registry-location/ddclient-api-container:latest
    container_name: ddclient-api
    ports:
      - "5000:5000"
    environment:
      - HEALTHCHECKS_URL=https://hc-ping.com
      - HEALTHCHECKS_ID=YOUR-UNIQUE-ID
    volumes:
      - ...
```

Replace `your-registry-location` with the actual registry location and `YOUR-UNIQUE-ID` with your actual `healthchecks.io` unique ID. Replace `./path/to/your/local/ddclient.conf` with the actual path to your custom `ddclient.conf` file on your local machine.

To run the Docker Compose setup, use the following command:

```bash
docker-compose up -d
```

## API Endpoints

The Flask application exposes the following API endpoints:

- **GET /status**: Returns the status of the last ddclient run.
- **GET /last_update**: Returns the last update time.
- **GET /last_status**: Returns the last status.
- **GET /last_ip**: Returns the the most recent IP address sent by `ddclient`.

## Files

- `Dockerfile`: Defines the Docker image.
- `ddclient.conf`: Default `ddclient` configuration file.
- `app.py`: Flask application that provides the API endpoints.
- `ddclient_wrapper.sh`: Wrapper script that runs `ddclient` and pings `healthchecks.io`.
- `docker-compose.yml`: Docker Compose configuration file.

## License

This project is licensed under the MIT License.

```plaintext
This README file provides an overview of the project, instructions for building and running the Docker container, details about the API endpoints, and a description of the key files in the project. Adjust the content as needed for your specific use case.
```
