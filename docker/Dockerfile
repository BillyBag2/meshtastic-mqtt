FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        mosquitto-clients && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install meshtastic && \
    pip3 install paho-mqtt

COPY test-mqtt-client.sh /root/test-mqtt-client.sh
#COPY test-mqtt.py /root/test-mqtt.py

ENV DEFAULT_HOST=mqtt.meshtastic.org
ENV DEFAULT_TOPIC=msh/EU_868/
ENV WILDCARD_TOPIC=msh/#
ENV DEFAULT_USER=meshdev
ENV DEFAULT_PASS=large4cats