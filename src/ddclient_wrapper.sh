#!/bin/bash
#
# DDClient Wrapper Script
#
# This script runs the ddclient service at regular intervals, logs the output,
# and sends a health check ping to healthchecks.io (if configured). The script runs
# indefinitely in a loop, sleeping for a specified interval between each iteration.
#
# Environment Variables:
#   DDCLIENT_INTERVAL           - The interval between ddclient runs (default: 360m).
#   HEALTHCHECKS_ID             - The unique ID for the healthchecks.io check.
#   HEALTHCHECKS_URL            - The base URL for healthchecks.io.
#   HEALTHCHECKS_CUSTOM_CA      - The base URL for healthchecks.io.
#
# Logs:
#   /var/log/ddclient.log       - Logs the output of ddclient runs.
#   /var/log/healthcheck.log    - Logs the status of health check pings.
#
# Configuration:
#   /etc/ddclient/ddclient.conf - The configuration file for ddclient.
#   /etc/ssl/certs/ca.pem       - The CA certificate file for secure communication.
#
# Usage:
#   Ensure the required environment variables are set before running the script.
#   The script will run indefinitely, executing ddclient and sending health check pings
#   at regular intervals.
#
# Example:
#   export HEALTHCHECKS_URL=https://example.com
#   export HEALTHCHECKS_ID=YOUR-UUID
#   ./ddclient_wrapper.sh
#
# Author:
#   Charles Smith
#
# License:
#   This script is licensed under the MIT License.
#

# Copy custom ddclient.conf from temp directory if present
if [ "/tmp/ddclient.conf" ]; then
    cp -r /tmp/ddclient.conf /etc/ddclient/ddclient.conf
    chmod 600 /etc/ddclient/ddclient.conf
    custom_conf="true"
fi

# Log file paths
DDCLIENT_LOG="/var/log/ddclient.log"
HEALTHCHECK_LOG="/var/log/healthcheck.log"

# Check if the user-specified ddclient interval environment variable was set
if [ -z "$DDCLIENT_INTERVAL" ]; then
    # Default interval to 360 minutes if not set
    INTERVAL=360m
else
    # Use the user-specified interval
    INTERVAL=$DDCLIENT_INTERVAL
fi

# Print environment variables for debugging purposes
echo "INFO:     [$(date +%Y-%m-%d_%H:%M:%S)] Starting ... "
echo
echo "INFO:     [$(date +%Y-%m-%d_%H:%M:%S)] DDClient Update Interval: $INTERVAL"
echo "INFO:     [$(date +%Y-%m-%d_%H:%M:%S)] DDClient Custom Configuration: $custom_conf"
echo "INFO:     [$(date +%Y-%m-%d_%H:%M:%S)] DDClient Log File: $DDCLIENT_LOG"
echo
echo "INFO:     [$(date +%Y-%m-%d_%H:%M:%S)] Healthchecks URL: $HEALTHCHECKS_URL"
echo "INFO:     [$(date +%Y-%m-%d_%H:%M:%S)] Healthchecks ID: $HEALTHCHECKS_ID"
if [ -z "$HEALTHCHECKS_CUSTOM_CA" ] || [[ "$HEALTHCHECKS_CUSTOM_CA" == "false" ]]; then
    HEALTHCHECKS_CUSTOM_CA="false"
fi
echo "INFO:     [$(date +%Y-%m-%d_%H:%M:%S)] Healthchecks Custom CA: $HEALTHCHECKS_CUSTOM_CA"
echo "INFO:     [$(date +%Y-%m-%d_%H:%M:%S)] Healthchecks Log File: $HEALTHCHECK_LOG"
echo

# Infinite loop to run ddclient at regular intervals
while true; do
    # Run ddclient and capture the output
    output=$(ddclient -daemon=0 --file /etc/ddclient/ddclient.conf 2>&1)

    # Print the output of ddclient to the log file with a timestamp
    echo "[DDCLIENT] | [$(date +%Y-%m-%d_%H:%M:%S)]: $output" >>$DDCLIENT_LOG

    # Check if the required environment variables for healthchecks.io are set
    if [ "$HEALTHCHECKS_URL" ] && [ "$HEALTHCHECKS_ID" ]; then

        # Send a ping to healthchecks.io
        if [[ "$HEALTHCHECKS_CUSTOM_CA" == "true" ]]; then
            echo "INFO:     [$(date +%Y-%m-%d_%H:%M:%S)] Pinging healthchecks with custom CA"
            output=$(curl --cacert /etc/ssl/certs/ca.pem -fsS -m 10 --retry 5 "$HEALTHCHECKS_URL/$HEALTHCHECKS_ID/$?")
        else
            output=$(curl --insecure -fsS -m 10 --retry 5 "$HEALTHCHECKS_URL/$HEALTHCHECKS_ID/$?")
        fi

        # Log the status of the healthcheck ping with a timestamp
        echo "[HEALTHCHECK] | [$(date +%Y-%m-%d_%H:%M:%S)]: $output" >>$HEALTHCHECK_LOG
        echo "INFO:     [$(date +%Y-%m-%d_%H:%M:%S)] Sent health check ping to $HEALTHCHECKS_URL/$HEALTHCHECKS_ID"
    else
        echo "INFO:     [$(date +%Y-%m-%d_%H:%M:%S)] Healthcheck not configured. Skipping health check ping."
    fi

    # Sleep for the specified interval before the next iteration
    sleep $INTERVAL
done
