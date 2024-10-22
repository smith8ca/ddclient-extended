"""
DDClient API

This FastAPI application provides an API to interact with the ddclient service.
It includes endpoints to get the status of the last ddclient run, the last update time,
the last status, and the most recent IP address sent by ddclient. Additionally, it pings
a healthchecks.io service with the status every time ddclient runs.

Functions:
    get_last_update_status(): Parses the last entry in the ddclient log that starts with 
                                [DDCLIENT] and returns the status string.
    get_last_update_timestamp(): Parses the last entry in the ddclient log that starts 
                                with [DDCLIENT] and returns the timestamp string.
    get_last_update_ip(): Parses the last entry in the ddclient log that starts with [DDCLIENT] 
                                and returns the IP address string.
    get_last_healthcheck(): Parses the last entry in the healthcheck log and returns the status string.
    last_update_status(): FastAPI route that returns the status of the last ddclient update.
    last_update_timestamp(): FastAPI route that returns the timestamp of the last ddclient update.
    last_update_ip(): FastAPI route that returns the IP address of the last ddclient update.
    last_healthcheck(): FastAPI route that returns the status of the last health check.

Routes:
    /last_update_status (GET): Returns the status of the last ddclient update.
    /last_update_timestamp (GET): Returns the timestamp of the last ddclient update.
    /last_update_ip (GET): Returns the IP address of the last ddclient update.
    /last_healthcheck (GET): Returns the status of the last health check.

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


def get_last_healthcheck():
    try:
        result = subprocess.run(
            ["tail", "-n", "1", "/var/log/healthcheck.log"],
            capture_output=True,
            text=True,
        )
        # Extract the status string using regex
        status_match = re.search(
            r"\[\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}\] \| (\w+)", result.stdout
        )
        if status_match:
            return status_match.group(1)
        else:
            return "No status found"
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


@app.get("/last_healthcheck")
async def last_healthcheck():
    status = get_last_healthcheck()
    return JSONResponse(content={"last_healthcheck": status})


def custom_openapi():
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
