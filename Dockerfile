# Use an official Debian runtime as a parent image
FROM debian:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Copy the Python requirements file
COPY src/requirements.txt /tmp/requirements.txt

# Install ddclient, Python, and FastAPI
RUN apt-get update && \
    apt-get install -y ddclient python3 python3-pip curl && \
    pip3 install -r tmp/requirements.txt --break-system-packages && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/requirements.txt

# Copy the default ddclient configuration file
COPY src/config/ddclient.conf /etc/ddclient/ddclient.conf

# Set permissions for the ddclient configuration file
RUN chmod 600 /etc/ddclient/ddclient.conf

# Copy the CA certificate file
COPY src/ssl/* /etc/ssl/certs/

# Set permissions for the CA certificate file
RUN chmod 644 /etc/ssl/certs/ca.pem

# Copy the FastAPI application
COPY src/main.py /app/main.py

# Copy the wrapper script
COPY src/ddclient_wrapper.sh /usr/local/bin/ddclient_wrapper.sh

# Make the wrapper script executable
RUN chmod +x /usr/local/bin/ddclient_wrapper.sh

# Expose the FastAPI port
EXPOSE 8000

# Run the wrapper script and FastAPI server
CMD ["sh", "-c", "/usr/local/bin/ddclient_wrapper.sh & uvicorn app.main:app --host 0.0.0.0"]