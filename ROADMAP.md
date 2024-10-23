# Project Roadmap

This document outlines the planned features, improvements, and milestones for the DDClient API Container project.

## Current Version

### [Unreleased]

#### Planned Features

- [ ] Add user authentication and authorization.
- [ ] Implement rate limiting for API endpoints.
- [ ] Integrate messaging capabilities using Gotify or Apprise.
- [ ] Implement a front end user interface.
- [ ] Allow users to leverage self-signed certificates for the FastAPI Uvicorn server.

#### Improvements

- [ ] Refactor codebase for better modularity and maintainability.
- [ ] Optimize Docker image size and build time.
- [ ] Improve test coverage and add more unit tests.

#### Milestones

- [ ] Release version 1.0.0 with all planned features and improvements.

## Past Versions

### [0.1.0] - 2023-10-01

#### Features

- Initial release of the DDClient API Container project.
- Added Dockerfile to define the Docker image.
- Added `ddclient.conf` as the default `ddclient` configuration file.
- Added `app.py` to provide the FastAPI application with API endpoints.
- Added `ddclient_wrapper.sh` to run `ddclient` and ping `healthchecks.io`.
- Added `docker-compose.yml` to provide Docker Compose configuration.
