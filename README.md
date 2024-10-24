<p align="center">
  <a href="https://github.com/smith8ca/ddclient-extended">
    <img src="https://github.com/smith8ca/ddclient-extended/blob/main/images/ddclient-extended-logo.png?raw=true" alt="ddclient-extended-logo" width="256px" />
  </a>
</p>

<h1 align="center">
  DDClient Extended
</h1>
</br>

<p align="center">
  <a href="https://github.com/ddclient/ddclient">ddclient</a> packaged into a Docker container with a <a href="https://fastapi.tiangolo.com/">FastAPI</a>-based backend API and optional integragion with <a href="https://healthchecks.io/">healthchecks.io</a>.
</p>

<p align="center">
  <img alt="GitHub License" src="https://img.shields.io/github/license/smith8ca/ddclient-extended"> 
  &nbsp;
  <a href="https://paypal.me/CharlesASmith" title="Donate"><img alt="GitHub Sponsors" src="https://img.shields.io/github/sponsors/smith8ca"></a> 
  &nbsp;
  <a href="https://hub.docker.com/r/chuck1041/ddclient-extended" title="Dockerhub"><img alt="Docker Image Size" src="https://img.shields.io/docker/image-size/chuck1041/ddclient-extended"></a> 
  &nbsp;
  <a href="https://github.com/smith8ca/ddclient-extended" title="Github"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/smith8ca/ddclient-extended"></a> 
</p>
</br>

# Features

- Runs `ddclient` to update dynamic DNS records.
- Exposes a FastAPI-based API to expose execution information.
- Pings `healthchecks.io` with the status of `ddclient` runs (see [API Endpoints](#api-endpoints)).
- Allows mounting a custom `ddclient.conf` configuration file.

&nbsp;

# Getting Started

## Prerequisites

- Docker
- Docker Compose (optional)

&nbsp;

> [!IMPORTANT]
> The default [`ddclient.conf`](src/config/ddclient.conf.example) file does not contain any valid DNS domain configurations and will result in nothing happening. While the default file can be used for testing, this container is designed to have a custom `ddclient.conf` file supplied as a mount.

&nbsp;

## With Docker

To run the container using Docker Compose, modify the sample [`docker-compose.yml`](docker-compose.yml) file to meet your requirements or create a `docker-compose.yml` with the following content:

```yaml
services:
  ddclient-api:
    image: ghcr.io/smith8ca/ddclient-extended:latest
    container_name: ddclient-api
    ports:
      - "8000:8000"
    environment:
      - DDCLIENT_INTERVAL=360m
      - HEALTHCHECKS_URL=YOUR-HC-URL
      - HEALTHCHECKS_ID=YOUR-UUID
    volumes:
      - /path/to/your/ddclient.conf:/tmp/ddclient.conf:ro
```

To launch with Docker Run:

```bash
docker run -d -p 8000:8000 --name ddclient-api \
    -e DDCLIENT_INTERVAL=360m \
    -e HEALTHCHECKS_URL=YOUR-HC-URL \
    -e HEALTHCHECKS_ID=YOUR-UUID \
    -v /path/to/your/ddclient.conf:/tmp/ddclient.conf:ro \
    ghcr.io/smith8ca/ddclient-extended:latest
```

Be sure to update the environment variables accordingly. See the [Environment Variables](#environment-variables) section for more information.

&nbsp;

## From Source

First, clone the repository:

```bash
git clone https://github.com/smith8ca/ddclient-extended.git
```

Build the Docker image by running the following:

```bash
docker build -t ddclient-extended .
```

&nbsp;

## Self-Signed Certificates

By default, the `curl` command used to ping healthchecks has the `--insecure` flag enabled to avoid issues with self-signed certificates typically used in self-hosted environments. Otherwise, the `curl` commands will fail. You can read more about this behavior [here](https://curl.se/docs/sslcerts.html).

If you are self-hosting Healthchecks and you would like the healthcheck pings to communicate over HTTPS, you may supply your Certificate Authority to the container by mounting a custom `ca.pem` file to `/etc/ssl/certs/ca.pem:ro` and setting the `HEALTHCHECKS_CUSTOM_CA` environment variable to `true` as shown below:

```yaml
services:
  ddclient-api:
    image: ghcr.io/smith8ca/ddclient-extended:latest
    container_name: ddclient-api
    ports:
      - "8000:8000"
    environment:
      - HEALTHCHECKS_URL=https://example.lan
      - HEALTHCHECKS_ID=YOUR-UUID
      - HEALTHCHECKS_CUSTOM_CA=true
    volumes:
      - /path/to/your/ca.pem:/etc/ssl/certs/ca.pem:ro
```

This will force the `curl` command to execute healthcheck pings over HTTPS using your certificate authority.

&nbsp;

## Environment Variables

The following environment variables can be used to configure the Docker container:

| **Variable**             | **Description**                               | **Default** | **Required** |
| ------------------------ | --------------------------------------------- | :---------: | :----------: |
| `DDCLIENT_INTERVAL`      | The interval between ddclient runs            |    360m     |      No      |
| `HEALTHCHECKS_URL`       | The base URL for healthchecks.io              |    _N/A_    |      No      |
| `HEALTHCHECKS_ID`        | The UUID for the healthchecks.io check        |    _N/A_    |      No      |
| `HEALTHCHECKS_CUSTOM_CA` | Whether to use a custom certificate authority |    false    |      No      |

&nbsp;

# API Endpoints

The FastAPI application exposes the following API endpoints:

- **GET /last_healthcheck_status**: Returns the status of the last health check.
- **GET /last_healthcheck_timestamp**: Returns the timestamp of the last health check.
- **GET /last_update_ip**: Returns the IP address of the last `ddclient` update.
- **GET /last_update_status**: Returns the status of the last `ddclient` update.
- **GET /last_update_timestamp**: Returns the timestamp of the last `ddclient` update.
- **POST /run_ddclient**: Manually triggers the `ddclient` to run once and returns the output.

## Accessing the API Documentation

FastAPI automatically generates interactive API documentation. You can access it at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

&nbsp;

# Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.

## Roadmap

To see the project's wishlist for upcoming features and planned improvements, please refer to the [ROADMAP.md](ROADMAP.md) file.

&nbsp;

# Credits

- **ddclient**: This project uses [ddclient](https://github.com/ddclient/ddclient), a Perl client used to update dynamic DNS entries for accounts on various DNS providers.
- **FastAPI**: This project uses [FastAPI](https://fastapi.tiangolo.com/), a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **Healthchecks**: This project is built to work with [healthchecks](https://github.com/healthchecks/healthchecks), an open-source cron job and background task monitoring service

&nbsp;

# License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
