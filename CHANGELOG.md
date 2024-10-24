# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Added a new endpoint `/last_healthcheck_timestamp` to return the timestamp of the last health check.
- Added a new endpoint `/run_ddclient` to manually trigger the `ddclient` to run once and return the output.
- Added a new endpoint `/last_healthcheck_status` to return the status of the last health check.
- Added a new endpoint `/last_update_ip` to return the IP address of the last `ddclient` update.
- Added a new endpoint `/last_update_timestamp` to return the timestamp of the last `ddclient` update.
- Added a new endpoint `/last_update_status` to return the status of the last `ddclient` update.
- Added environment variables `DDCLIENT_INTERVAL`, `HEALTHCHECKS_URL`, and `HEALTHCHECKS_ID` to configure the Docker container.
- Added a section in the README to explain the Docker environment variables in a table format.
- Added a "Credits" section in the README to acknowledge the creators of `ddclient` and `FastAPI`.

### Changed

- Updated the README file to include instructions for running the project using Docker Compose.
- Updated the README file to provide comprehensive instructions and information about the project.

### Fixed

- Fixed various typos and formatting issues in the README file.

## [0.1.0] - 2023-10-01

### Added

- Initial release of the DDClient API Container project.
- Added Dockerfile to define the Docker image.
- Added `ddclient.conf` as the default `ddclient` configuration file.
- Added `app.py` to provide the FastAPI application with API endpoints.
- Added `ddclient_wrapper.sh` to run `ddclient` and ping `healthchecks.io`.
- Added `docker-compose.yml` to provide Docker Compose configuration.
