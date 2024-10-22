# DDClient API Container

This project packages `ddclient` into a Docker container with a FastAPI-based API. The container allows you to run `ddclient` and expose an API to get the last update, last status, the most recent IP address, and health check status. Additionally, it implements optional pings to a `healthchecks.io` service with the status every time `ddclient` runs.

## Features

- Runs `ddclient` to update dynamic DNS records.
- Exposes a FastAPI-based API to get the last update, last status, the most recent IP address, and health check status.
- Pings `healthchecks.io` with the status of `ddclient` runs.
- Allows optional overwriting of the default `ddclient.conf` file by mounting a custom configuration file.

## Prerequisites

- Docker
- Docker Compose (optional, for using Docker Compose)
- Python 3.7+ (for running FastAPI locally)

## Getting Started

### Run the Docker Container

#### Run with Default Configuration

To run the container with the default `ddclient.conf` configuration, use the following command:

```bash
docker run -d -p 8000:8000 --name ddclient-api \
    -e HEALTHCHECKS_URL=https://hc-ping.com \
    -e HEALTHCHECKS_ID=YOUR-UNIQUE-ID \
    ddclient-api-container
```

Replace `YOUR-UNIQUE-ID` with your actual healthchecks.io unique ID.

#### Run with Custom Configuration

The container is designed to run with a custom `ddclient.conf` configuration. To do this, mount your custom `ddclient.conf` file as a volume as shown below:

```bash
docker run -d -p 8000:8000 --name ddclient-api \
    -e HEALTHCHECKS_URL=https://hc-ping.com \
    -e HEALTHCHECKS_ID=YOUR-UNIQUE-ID \
    -v /path/to/your/ddclient.conf:/etc/ddclient/ddclient.conf \
    ddclient-api-container
```

Replace `/path/to/your/ddclient.conf` with the actual path to the custom ddclient configuration file on your local machine. Check out the example [`ddclient.conf`](src/config/ddclient.conf.example) file to understand more.

### Run with Docker Compose

You can also run the container using Docker Compose. Create a `docker-compose.yml` file with the following content:

```yaml
services:
  ddclient-api:
    image: your-registry-location/ddclient-api-container:latest
    container_name: ddclient-api
    ports:
      - "8000:8000"
    environment:
      - HEALTHCHECKS_URL=https://hc-ping.com
      - HEALTHCHECKS_ID=YOUR-UNIQUE-ID
    volumes:
      - /path/to/your/ddclient.conf:/etc/ddclient/ddclient.conf
```

Replace `YOUR-UNIQUE-ID` with your actual healthchecks.io unique ID. Replace `/path/to/your/ddclient.conf` with the actual path to the custom ddclient configuration file on your local machine.

Alternatively, you can modify the sample [`docker-compose.yml`](docker-compose.yml) file to meet your requirements. When doing this, be sure to also adapt the provided example [environment file](example.env) with your respective variable values as well.

To run the Docker Compose setup, use the following command:

```bash
docker-compose up -d
```

### Environment Variables

The following environment variables can be used to configure the Docker container:

| **Variable**        | **Description**                             | **Default** | **Required** |
| ------------------- | ------------------------------------------- | :---------: | :----------: |
| `DDCLIENT_INTERVAL` | The interval between ddclient runs          |    360m     |      No      |
| `HEALTHCHECKS_URL`  | The base URL for healthchecks.io            |    None     |      No      |
| `HEALTHCHECKS_ID`   | The unique ID for the healthchecks.io check |    None     |      No      |

## API Endpoints

The FastAPI application exposes the following API endpoints:

- **GET /last_update_status**: Returns the status of the last `ddclient` update.
- **GET /last_update_timestamp**: Returns the timestamp of the last `ddclient` update.
- **GET /last_update_ip**: Returns the IP address of the last `ddclient` update.
- **GET /last_healthcheck**: Returns the status of the last health check.

### Accessing the API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Files

- `Dockerfile`: Defines the Docker image.
- `ddclient.conf`: Default ddclient configuration file.
- `app.py`: FastAPI application that provides the API endpoints.
- `ddclient_wrapper.sh`: Wrapper script that runs ddclient and pings healthchecks.io.
- `docker-compose.yml`: Docker Compose configuration file.

## Credits

- **ddclient**: This project uses [ddclient](https://github.com/ddclient/ddclient), a Perl client used to update dynamic DNS entries for accounts on various DNS providers.
- **FastAPI**: This project uses [FastAPI](https://fastapi.tiangolo.com/), a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## License

This project is licensed under the [MIT License](LICENSE).
