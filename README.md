# DDClient Extended

This project packages [ddclient](https://github.com/ddclient/ddclient) into a Docker container with a [FastAPI](https://fastapi.tiangolo.com/)-based API. The container allows you to run `ddclient` and expose an API to get the last update, last status, the most recent IP address, and health check status. Additionally, it implements optional pings to a [`healthchecks.io`](https://healthchecks.io/) service with the status every time `ddclient` runs.

- [DDClient Extended](#ddclient-extended)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
    - [Build the Docker Image](#build-the-docker-image)
    - [Run the Docker Container](#run-the-docker-container)
      - [Run with Default Configuration](#run-with-default-configuration)
      - [Run with Custom Configuration](#run-with-custom-configuration)
    - [Run with Docker Compose](#run-with-docker-compose)
    - [Self-Signed Certificates](#self-signed-certificates)
    - [Environment Variables](#environment-variables)
  - [API Endpoints](#api-endpoints)
    - [Accessing the API Documentation](#accessing-the-api-documentation)
  - [Files](#files)
  - [Roadmap](#roadmap)
  - [Credits](#credits)
  - [License](#license)

&nbsp;

## Features

- Runs `ddclient` to update dynamic DNS records.
- Exposes a FastAPI-based API to get the last update, last status, the most recent IP address, and health check status.
- Pings `healthchecks.io` with the status of `ddclient` runs.
- Allows optional overwriting of the default `ddclient.conf` file by mounting a custom configuration file.

&nbsp;

## Prerequisites

- Docker
- Docker Compose (optional, for using Docker Compose)
- Python 3.7+ (for running FastAPI locally)

&nbsp;

## Getting Started

### Build the Docker Image

To build the Docker image, run the following command:

```bash
docker build -t ddclient-api-container .
```

&nbsp;

### Run the Docker Container

#### Run with Default Configuration

To run the container with the default `ddclient.conf` configuration, use the following command:

```bash
docker run -d -p 8000:8000 --name ddclient-api \
    -e DDCLIENT_INTERVAL=360m \
    -e HEALTHCHECKS_URL=https://hc-ping.com \
    -e HEALTHCHECKS_ID=YOUR-UNIQUE-ID \
    ddclient-api-container
```

Replace `YOUR-UNIQUE-ID` with your actual healthchecks.io unique ID.

&nbsp;

#### Run with Custom Configuration

The container is designed to run with a custom `ddclient.conf` configuration. To do this, mount your custom `ddclient.conf` file as a volume as shown below:

```bash
docker run -d -p 8000:8000 --name ddclient-api \
    -e DDCLIENT_INTERVAL=360m \
    -e HEALTHCHECKS_URL=https://hc-ping.com \
    -e HEALTHCHECKS_ID=YOUR-UNIQUE-ID \
    -v /path/to/your/ddclient.conf:/tmp/ddclient.conf:ro \
    ddclient-api-container
```

Replace `/path/to/your/ddclient.conf` with the actual path to the custom ddclient configuration file on your local machine. Check out the example [`ddclient.conf`](src/config/ddclient.conf.example) file to understand more.

&nbsp;

### Run with Docker Compose

You can also run the container using Docker Compose. Create a `docker-compose.yml` file with the following content:

```yaml
services:
  ddclient-api:
    image: ddclient-api-container:latest
    container_name: ddclient-api
    ports:
      - "8000:8000"
    environment:
      - DDCLIENT_INTERVAL=360m
      - HEALTHCHECKS_URL=https://hc-ping.com
      - HEALTHCHECKS_ID=YOUR-UNIQUE-ID
```

Replace `YOUR-UNIQUE-ID` with your actual healthchecks.io unique ID. Replace `/path/to/your/ddclient.conf` with the actual path to the custom ddclient configuration file on your local machine.

Alternatively, you can modify the sample [`docker-compose.yml`](docker-compose.yml) file to meet your requirements. When doing this, be sure to also adapt the provided example [environment file](example.env) with your respective variable values as well.

To run the Docker Compose setup, use the following command:

```bash
docker-compose up -d
```

&nbsp;

### Self-Signed Certificates

By default, the `curl` command that pings healthchecks has the `--insecure` flag enabled to avoid issues with self-hosted environments. Otherwise, the `curl` commands will fail. You can read more about this behavior [here](https://curl.se/docs/sslcerts.html).

If you are self-hosting Healthchecks and you would like the healthcheck pings to communicate over HTTPS, you will need to supply your Certificate Authority store to the container by mounting your `ca.pem` file to `/etc/ssl/certs/ca.pem:ro` and setting the `HEALTHCHECKS_CUSTOM_CA` environment variable to `true` as shown below:

```yaml
services:
  ddclient-api:
    image: ddclient-api-container:latest
    container_name: ddclient-api
    ports:
      - "8000:8000"
    environment:
      - HEALTHCHECKS_URL=https://example.lan
      - HEALTHCHECKS_ID=YOUR-UNIQUE-ID
      - HEALTHCHECKS_CUSTOM_CA=true
    volumes:
      - /path/to/your/ca.pem:/etc/ssl/certs/ca.pem:ro
```

This will force the `curl` command to execute healthcheck pings over HTTPS using your certificate authority.

&nbsp;

### Environment Variables

The following environment variables can be used to configure the Docker container:

| **Variable**             | **Description**                               | **Default** | **Required** |
| ------------------------ | --------------------------------------------- | :---------: | :----------: |
| `DDCLIENT_INTERVAL`      | The interval between ddclient runs            |    360m     |      No      |
| `HEALTHCHECKS_URL`       | The base URL for healthchecks.io              |    _N/A_    |      No      |
| `HEALTHCHECKS_ID`        | The unique ID for the healthchecks.io check   |    _N/A_    |      No      |
| `HEALTHCHECKS_CUSTOM_CA` | Whether to use a custom certificate authority |    false    |      No      |

&nbsp;

## API Endpoints

The FastAPI application exposes the following API endpoints:

- **GET /last_healthcheck_status**: Returns the status of the last health check.
- **GET /last_healthcheck_timestamp**: Returns the timestamp of the last health check.
- **GET /last_update_ip**: Returns the IP address of the last `ddclient` update.
- **GET /last_update_status**: Returns the status of the last `ddclient` update.
- **GET /last_update_timestamp**: Returns the timestamp of the last `ddclient` update.
- **POST /run_ddclient**: Manually triggers the `ddclient` to run once and returns the output.

### Accessing the API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

&nbsp;

## Files

- `Dockerfile`: Defines the Docker image.
- `ddclient.conf`: Default ddclient configuration file.
- `app.py`: FastAPI application that provides the API endpoints.
- `ddclient_wrapper.sh`: Wrapper script that runs ddclient and pings healthchecks.io.
- `docker-compose.yml`: Docker Compose configuration file.

&nbsp;

## Roadmap

For upcoming features and planned improvements, please refer to the [ROADMAP.md](ROADMAP.md) file.

&nbsp;

## Credits

- **ddclient**: This project uses [ddclient](https://github.com/ddclient/ddclient), a Perl client used to update dynamic DNS entries for accounts on various DNS providers.
- **FastAPI**: This project uses [FastAPI](https://fastapi.tiangolo.com/), a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Healthchecks**: This project is built to work with [healthchecks](https://github.com/healthchecks/healthchecks), an open-source cron job and background task monitoring service

&nbsp;

## License

This project is licensed under the [MIT License](LICENSE).
