"""
DDClient API

This FastAPI application provides an API to interact with the ddclient service.
It includes endpoints to get the status of the last ddclient run, the last update time,
the last status, and the most recent IP address sent by ddclient. Additionally, it pings
a healthchecks.io service with the status every time ddclient runs.

Functions:
    get_last_update_status(): Parses the last entry in the ddclient log that starts with [DDCLIENT] and returns the status string.
    get_last_update_timestamp(): Parses the last entry in the ddclient log that starts with [DDCLIENT] and returns the timestamp string.
    get_last_update_ip(): Parses the last entry in the ddclient log that starts with [DDCLIENT] and returns the IP address string.
    get_last_healthcheck_status(): Parses the last entry in the healthcheck log and returns the status string.
    get_last_healthcheck_timestamp(): Parses the last entry in the healthcheck log and returns the timestamp string.
    run_ddclient(): Manually triggers the ddclient to run once and returns the output.
    last_update_status(): FastAPI route that returns the status of the last ddclient update.
    last_update_timestamp(): FastAPI route that returns the timestamp of the last ddclient update.
    last_update_ip(): FastAPI route that returns the IP address of the last ddclient update.
    last_healthcheck_status(): FastAPI route that returns the status of the last health check.
    last_healthcheck_timestamp(): FastAPI route that returns the timestamp of the last health check.

Routes:
    /last_update_status (GET): Returns the status of the last ddclient update.
    /last_update_timestamp (GET): Returns the timestamp of the last ddclient update.
    /last_update_ip (GET): Returns the IP address of the last ddclient update.
    /last_healthcheck_status (GET): Returns the status of the last health check.
    /last_healthcheck_timestamp (GET): Returns the timestamp of the last health check.
    /run_ddclient (POST): Manually triggers the ddclient to run once and returns the output.

Usage:
    Run this script to start the FastAPI server and expose the API endpoints.
    The server listens on all available IP addresses (0.0.0.0) and port 8000.
"""

import re
import subprocess

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

app = FastAPI()


def get_last_update_status():
    """
    Retrieves the last update status from the ddclient log file.

    This function runs a subprocess to grep for entries starting with "[DDCLIENT]"
    in the /var/log/ddclient.log file. It then extracts the last entry and uses
    a regular expression to find the status string.

    Returns:
        str: The last update status if found, otherwise "No status found".
             If an exception occurs, returns the exception message.
    """
    try:
        result = subprocess.run(
            ["grep", "[DDCLIENT]", "/var/log/ddclient.log"],
            capture_output=True,
            text=True,
        )

        # Extract the last entry starting with [DDCLIENT]
        last_entry = result.stdout.strip().split("\n")[-1]

        # Extract the status string using regex
        status_match = re.search(
            r"\[DDCLIENT\] \| \[\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}\]: (\w+):",
            last_entry,
        )

        if status_match:
            return status_match.group(1)
        else:
            return "No status found"
    except Exception as e:
        return str(e)


def get_last_update_timestamp():
    """
    Retrieves the last update timestamp from the ddclient log.

    This function runs a subprocess to grep for lines containing "[DDCLIENT]"
    in the ddclient log file located at "/var/log/ddclient.log". It then extracts
    the last entry and uses a regular expression to find the timestamp in the format
    "YYYY-MM-DD_HH:MM:SS".

    Returns:
        str: The extracted timestamp if found, otherwise "No timestamp found".
             If an exception occurs, the exception message is returned.
    """
    try:
        result = subprocess.run(
            ["grep", "[DDCLIENT]", "/var/log/ddclient.log"],
            capture_output=True,
            text=True,
        )

        # Extract the last entry starting with [DDCLIENT]
        last_entry = result.stdout.strip().split("\n")[-1]

        # Extract the timestamp string using regex
        timestamp_match = re.search(
            r"\[DDCLIENT\] \| \[(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2})\]:", last_entry
        )

        if timestamp_match:
            return timestamp_match.group(1)
        else:
            return "No timestamp found"
    except Exception as e:
        return str(e)


def get_last_update_ip():
    """
    Retrieves the last updated IP address from the ddclient log.

    This function runs a subprocess to grep for lines containing "[DDCLIENT]"
    in the /var/log/ddclient.log file. It then extracts the last entry from
    the result and uses a regular expression to find the IP address.

    Returns:
        str: The last updated IP address if found, otherwise a message indicating
             no IP address was found or an error message if an exception occurs.
    """
    try:
        result = subprocess.run(
            ["grep", "[DDCLIENT]", "/var/log/ddclient.log"],
            capture_output=True,
            text=True,
        )

        # Extract the last entry starting with [DDCLIENT]
        last_entry = result.stdout.strip().split("\n")[-1]

        # Extract the IP address string using regex
        ip_match = re.search(
            r"IP address set to (\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)", last_entry
        )

        if ip_match:
            return ip_match.group(1)
        else:
            return "No IP address found"
    except Exception as e:
        return str(e)


def get_last_healthcheck_status():
    """
    Retrieves the last health check status from the healthcheck log file.

    This function runs a shell command to read the last line of the
    /var/log/healthcheck.log file and extracts the status string using a
    regular expression.

    Returns:
        str: The extracted status string if found, otherwise "No status found".
             If an exception occurs, returns the exception message.
    """
    try:
        result = subprocess.run(
            ["tail", "-n", "1", "/var/log/healthcheck.log"],
            capture_output=True,
            text=True,
        )

        # Extract the status string using regex
        status_match = re.search(
            r"\[HEALTHCHECK\] \| \[\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}\]: (.+)",
            result.stdout,
        )

        if status_match:
            return status_match.group(1)
        else:
            return "No status found"
    except Exception as e:
        return str(e)


def get_last_healthcheck_timestamp():
    """
    Retrieves the last health check timestamp from the healthcheck log file.

    This function runs a shell command to get the last line of the healthcheck log file
    located at /var/log/healthcheck.log. It then extracts the timestamp from the log entry
    using a regular expression.

    Returns:
        str: The extracted timestamp in the format 'YYYY-MM-DD_HH:MM:SS' if found,
             otherwise returns "No timestamp found". If an exception occurs, returns
             the exception message as a string.
    """
    try:
        result = subprocess.run(
            ["tail", "-n", "1", "/var/log/healthcheck.log"],
            capture_output=True,
            text=True,
        )
        # Extract the timestamp string using regex
        timestamp_match = re.search(
            r"\[HEALTHCHECK\] \| \[(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2})\]:",
            result.stdout,
        )
        if timestamp_match:
            return timestamp_match.group(1)
        else:
            return "No timestamp found"
    except Exception as e:
        return str(e)


def run_ddclient():
    """
    Executes the ddclient command with specified arguments and captures its output.

    This function runs the ddclient command with the following arguments:
    - `-daemon=0`: Runs ddclient in the foreground.
    - `--file /etc/ddclient/ddclient.conf`: Specifies the configuration file to use.

    Additionally, it writes the output to the ddclient log file in the format:
    [DDCLIENT] | [$(date +%Y-%m-%d_%H:%M:%S)]: $output

    Returns:
        str: The standard output from the ddclient command if it runs successfully.
        str: The exception message if an error occurs during the execution of the command.
    """
    try:
        result = subprocess.run(
            ["ddclient", "-daemon=0", "--file", "/etc/ddclient/ddclient.conf"],
            capture_output=True,
            text=True,
        )

        output = result.stdout

        # Write to the ddclient log file
        with open("/var/log/ddclient.log", "a") as log_file:
            log_file.write(
                f"[DDCLIENT] | [{subprocess.run(['date', '+%Y-%m-%d_%H:%M:%S'], capture_output=True, text=True).stdout.strip()}]: {output}\n"
            )

        return output
    except Exception as e:
        return str(e)


@app.get("/last_update_status")
async def last_update_status():
    status = get_last_update_status()
    return JSONResponse(content={"last_update_status": status})


@app.get("/last_update_timestamp")
async def last_update_timestamp():
    timestamp = get_last_update_timestamp()
    return JSONResponse(content={"last_update_timestamp": timestamp})


@app.get("/last_update_ip")
async def last_update_ip():
    ip = get_last_update_ip()
    return JSONResponse(content={"last_update_ip": ip})


@app.get("/last_healthcheck_status")
async def last_healthcheck_status():
    status = get_last_healthcheck_status()
    return JSONResponse(content={"last_healthcheck_status": status})


@app.get("/last_healthcheck_timestamp")
async def last_healthcheck_timestamp():
    timestamp = get_last_healthcheck_timestamp()
    return JSONResponse(content={"last_healthcheck_timestamp": timestamp})


@app.post("/run_ddclient")
async def run_ddclient_endpoint():
    output = run_ddclient()
    return JSONResponse(content={"output": output})


def custom_openapi():
    """
    Generates and caches the OpenAPI schema for the FastAPI application.

    This function checks if the OpenAPI schema has already been generated and cached
    in the `app.openapi_schema` attribute. If it has, the cached schema is returned.
    If not, it generates a new OpenAPI schema using the `get_openapi` function, caches
    it in the `app.openapi_schema` attribute, and then returns the newly generated schema.

    Returns:
        dict: The OpenAPI schema for the FastAPI application.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="DDClient API",
        version="1.0.0",
        description="API for interacting with the ddclient service.",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
