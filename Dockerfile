FROM debian:latest

ENV DEBIAN_FRONTEND=noninteractive

COPY src/config/ddclient.conf.example /etc/ddclient/ddclient.conf
COPY src/ddclient_wrapper.sh /usr/local/bin/ddclient_wrapper.sh
COPY src/main.py /app/main.py
COPY src/requirements.txt /tmp/requirements.txt

RUN apt-get update && \
    apt-get install -y ddclient python3 python3-pip curl && \
    pip3 install --no-cache-dir --upgrade -r tmp/requirements.txt --break-system-packages && \
    chmod 600 /etc/ddclient/ddclient.conf && \
    chmod +x /usr/local/bin/ddclient_wrapper.sh && \
    apt-get clean && \
    pip3 cache purge && \
    rm -rf /var/lib/apt/lists/* /tmp/requirements.txt

# Expose the FastAPI port
EXPOSE 8000

# Run the wrapper script and FastAPI server
CMD ["sh", "-c", "/usr/local/bin/ddclient_wrapper.sh & uvicorn app.main:app --host 0.0.0.0"]