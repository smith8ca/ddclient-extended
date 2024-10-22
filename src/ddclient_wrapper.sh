#!/bin/bash
#
# DDClient Wrapper Script
#
# This script runs the ddclient service at regular intervals, logs the output,
# and sends a health check ping to healthchecks.io. The script runs indefinitely
# in a loop, sleeping for a specified interval between each iteration.
#
# Environment Variables:
#   HEALTHCHECKS_URL    - The base URL for healthchecks.io.
#   HEALTHCHECKS_ID     - The unique ID for the healthchecks.io check.
#
# Logs:
#   /var/log/ddclient.log      - Logs the output of ddclient runs.
#   /var/log/healthcheck.log   - Logs the status of health check pings.
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
#   export HEALTHCHECKS_URL=https://hc-ping.com
#   export HEALTHCHECKS_ID=YOUR-UNIQUE-ID
#   ./ddclient_wrapper.sh
#
# Variables:
#   DDCLIENT_LOG        - Path to the ddclient log file.
#   HEALTHCHECK_LOG     - Path to the health check log file.
#   INTERVAL            - Time interval between each ddclient run (default: 360m).
#
# Author:
#   Charles Smith
#
# License:
#   This script is licensed under the MIT License.
#

DDCLIENT_LOG="/var/log/ddclient.log"
HEALTHCHECK_LOG="/var/log/healthcheck.log"
INTERVAL=360m

# Check if the required environment variables are set
if [ -z "$HEALTHCHECKS_URL" ] || [ -z "$HEALTHCHECKS_ID" ]; then
    echo "Error: HEALTHCHECKS_URL and HEALTHCHECKS_ID environment variables must be set."
    exit 1
fi

echo "Environment variables set ... "
echo "Healthchecks URL: $HEALTHCHECKS_URL"
echo "Healthchecks ID: $HEALTHCHECKS_ID"
echo

while true; do
    # Run ddclient and capture the output
    output=$(ddclient -daemon=0 --file /etc/ddclient/ddclient.conf 2>&1)

    # Print the output of ddclient
    echo "[DDCLIENT] | [$(date +%Y-%m-%d_%H:%M:%S)]: $output" >>$DDCLIENT_LOG

    # Send a ping to healthchecks.io
    output=${curl--cacert /etc/ssl/certs/ca.pem -fsS -m 10 --retry 5 -o /dev/null "$HEALTHCHECKS_URL/$HEALTHCHECKS_ID/$?"}

    # Log the status of the healthcheck ping
    echo "[TIMESTAMP] | $output" >>$HEALTHCHECK_LOG

    # Sleep for a specified interval before the next iteration
    sleep $INTERVAL
done
